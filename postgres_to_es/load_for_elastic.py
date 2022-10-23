from my_config import ElacticConfig
from condition import RedisStorage
from backoff import backoff

from typing import Generator, Optional, Callable
from elasticsearch import Elasticsearch, helpers


class ElacticLoad:

    def __init__(self,
                 config: ElacticConfig,
                 state: RedisStorage,
                 elastic_connection: Optional[Elasticsearch] = None):
        self.config = config
        self.connect = elastic_connection
        self.state = state

    @property
    def elastic_connection(self) -> Elasticsearch:
        """Вернуть текущее подключение для ES или инициализировать новое"""
        if self.connect is None or not self.connect.ping():
            self.connect = self._create_connection()

        return self.connect

    @backoff()
    def _create_connection(self) -> Elasticsearch:
        """Подключение к ES"""
        return Elasticsearch(hosts=[f'{self.config.host}:{self.config.port}'])

    def _transform_data(self, raw_data: Generator, structure: Callable, name_index: str) -> Generator:
        """Создание итератора и сохранение состояния"""

        for row in raw_data:
            data_dict = structure(**row).dict()
            data_dict['_id'] = data_dict['id']
            if data_dict['director'] is None:
                data_dict['director'] = []

            self.state.save_state(name_index, str(row['modified'])[:-3])

            yield data_dict

    def load_data(self, name_index: str, data: Generator, structure: Callable):
        """Загрузка данных в ES"""
        docs = self._transform_data(data, structure, name_index)
        helpers.bulk(
            client=self.elastic_connection,
            actions=docs,
            index=name_index
        )

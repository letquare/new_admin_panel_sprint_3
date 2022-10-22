from my_config import RedisConfig
from backoff import backoff

from redis import Redis


class RedisStorage:
    """Класс для хранения состояния при работе с данными,
    чтобы постоянно не перечитывать данные с начала."""
    def __init__(self, config: RedisConfig):
        self.config = config
        self.connect = self._connection()

    @backoff()
    def _connection(self):
        """"Ссоздает подключения к Redis"""
        return Redis(**self.config.dict())

    def save_state(self, key: str, value: str) -> None:
        """Установить состояние для определённого ключа"""
        self.connect.set(key, value.encode())

    def retrieve_state(self, key: str, default=None):
        """Получить состояние по определённому ключу"""
        data = self.connect.get(key)
        if data:
            return data.decode()
        return default

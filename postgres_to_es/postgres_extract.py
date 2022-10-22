import psycopg2
from psycopg2.extensions import connection
from psycopg2.extras import RealDictCursor
from typing import Generator

from my_config import PostgresDsl
from backoff import backoff


from dotenv import load_dotenv
load_dotenv()


class PostgresExtration:

    def __init__(self, config: PostgresDsl):

        self.config = config
        self.connect = self._connection()

    @backoff()
    def _connection(self) -> connection:
        """Создает соединение с Postgres"""
        return psycopg2.connect(**self.config.dict(),
                                cursor_factory=RealDictCursor)

    def extract(self, name_table, _from) -> Generator:
        """Получение данных из Postgres"""
        with self.connect.cursor() as cursor:
            cursor.execute(name_table(_from))
            for records in cursor:
                yield records

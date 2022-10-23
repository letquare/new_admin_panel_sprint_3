"""Модуль для переноса данных из SQLite в Postgres"""
import sqlite3
import psycopg2
import os

from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor, execute_batch

from query_for_postgres import (
    create_schema,
    create_table_film_work,
    create_table_person,
    create_table_genre,
    create_table_person_film_work,
    create_table_genre_film_work
)
from contextlib import contextmanager
from typing import List
from dotenv import load_dotenv

load_dotenv()


class ConnectionMixin:
    """Миксин-класс для создания подключения"""
    def __init__(self, conn):
        self.conn = conn


class PostgresSaver(ConnectionMixin):
    """Класс для сохранения данных в Postgres"""
    def save_all_data(self, data: List[sqlite3.Row], table_name: str) -> None:
        """
        Метод сохраняет данные из SQLite в Postgres
        :param data: List[sqlite3.Row] Данные которые нужно сохранить
        :param table_name: str Название таблицы
        :return: None
        """
        with self.conn.cursor() as cursor:
            try:
                for values in data:
                    name_column = tuple(value for value in dict(values[0]))
                    count_column = tuple('%s' for _ in range(len(name_column)))

                    query = """
                        INSERT INTO {0} {1}
                        VALUES {2}
                        ON CONFLICT (id) DO NOTHING"""\
                        .format(table_name,
                                str(name_column).translate({39: None}),
                                str(count_column).translate({39: None})
                                ).replace(
                        'created_at', 'created'
                    ).replace('updated_at', 'modified')

                    execute_batch(cursor, query, values, page_size=100)

            except (psycopg2.Error, TypeError) as exc:
                print(exc)
                self.conn.rollback()
            else:
                self.conn.commit()

    def create_table(self):
        with self.conn.cursor() as cursor:
            for command in (create_schema, create_table_film_work,
                            create_table_person,
                            create_table_genre,
                            create_table_person_film_work,
                            create_table_genre_film_work
                            ):
                cursor.execute(command())


class SQLiteExtractor(ConnectionMixin):
    """Класс для получения данных из SQLite"""
    def extract_movies(self, table_name: str) -> List[sqlite3.Row]:
        """
        Метод для получения данных из таблицы что передали в первом аргументе
        :param table_name: str Название таблицы в БД
        :return: List[Generator] Данные из БД
        """
        try:
            self.conn.row_factory = sqlite3.Row
            with self._cursor_context() as cursor:
                sql_query = """select * from {};""".format(table_name)
                cursor.execute(sql_query)
                while True:
                    record = cursor.fetchmany(100)
                    if record:
                        yield record
                    else:
                        break
        except sqlite3.Error:
            exit()

    @contextmanager
    def _cursor_context(self):
        """Вспомогательный метод для закрытия соединения cursor через with"""
        cursor = self.conn.cursor()
        yield cursor

        cursor.close()


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_extractor = SQLiteExtractor(connection)

    postgres_saver.create_table()

    for table in ('film_work', 'person', 'genre',
                  'genre_film_work', 'person_film_work'):

        data = sqlite_extractor.extract_movies(table)
        postgres_saver.save_all_data(data, table)


if __name__ == '__main__':
    dsl = {'dbname': os.environ.get('POSTGRES_DB'),
           'user': os.environ.get('POSTGRES_USER'),
           'password': os.environ.get('POSTGRES_PASSWORD'),
           'host': os.environ.get('DB_HOST'),
           'port': os.environ.get('DB_PORT')
           }
    with sqlite3.connect('db.sqlite') as sqlite_conn, psycopg2.connect(
            **dsl, cursor_factory=DictCursor
    ) as pg_connect:
        load_from_sqlite(sqlite_conn, pg_conn=pg_connect)

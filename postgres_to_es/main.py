import logging
import time

from postgres_extract import PostgresExtration
from load_for_elastic import ElacticLoad
from condition import RedisStorage
from query import movies
from structure import MoviesStructure
from my_config import REDISCON, POSTGRES, ELASTICSEARCH, SLEEP_TIME

from datetime import datetime

redis_state = RedisStorage(config=REDISCON)
elastic_loader = ElacticLoad(config=ELASTICSEARCH, state=redis_state)
postgres_extract = PostgresExtration(config=POSTGRES)

logger = logging.getLogger('my_log_lord')


def etl():
    """Оснавная функция которая запускает весь процесс"""
    while True:
        logger.info('Checking changes in the database and then uploading to ES')
        save_data = redis_state.retrieve_state(movies.__name__,
                                               default=str(datetime.min))
        data_extract = postgres_extract.extract(name_table=movies,
                                                _from=save_data
                                                )
        elastic_loader.load_data(name_index=movies.__name__,
                                 data=data_extract,
                                 structure=MoviesStructure
                                 )

        logger.info("Now I'll get some sleep and then I'll go check it out.")
        time.sleep(SLEEP_TIME)


if __name__ == '__main__':
    etl()

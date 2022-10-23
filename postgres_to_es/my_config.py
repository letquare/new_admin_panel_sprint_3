from pydantic import BaseSettings, BaseConfig
from dotenv import load_dotenv

load_dotenv()


class PostgresDsl(BaseSettings):
    dbname: str
    user: str
    password: str
    host: str
    port: str

    class Config:
        env_prefix = 'my_prefix_'
        fields = {
            'dbname': {
                'env': 'postgres_db'
            },
            'user': {
                'env': 'postgres_user'
            },
            'password': {
                'env': 'postgres_password'
            },
            'host': {
                'env': 'db_host'
            },
            'port': {
                'env': 'db_port'
            }
        }


class ElacticConfig(BaseSettings):
    host: str
    port: str

    class Config:
        env_prefix = 'my_prefix_'
        fields = {
            'host': {
                'env': 'elastic_host'
            },
            'port': {
                'env': 'elastic_port'
            }
        }


class RedisConfig(BaseSettings):
    host: str
    port: str

    class Config:
        env_prefix = 'my_prefix_'
        fields = {
            'host': {
                'env': 'redis_host'
            },
            'port': {
                'env': 'redis_port'
            }
        }


ELASTICSEARCH = ElacticConfig()
REDISCON = RedisConfig()
POSTGRES = PostgresDsl()
SLEEP_TIME = 10

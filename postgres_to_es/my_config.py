from pydantic import BaseSettings, Field
from dotenv import load_dotenv

load_dotenv()


class PostgresDsl(BaseSettings):
    dbname: str = Field(env='DB_NAME')
    user: str = Field(env='DB_USER')
    password: str = Field(env='DB_PASSWORD')
    host: str = Field(env='DB_HOST')
    port: str = Field(env='DB_PORT')


class ElacticConfig(BaseSettings):
    host: str = Field(env='ELACTIC_HOST')
    port: str = Field(env='ELACTIC_PORT')


class RedisConfig(BaseSettings):
    host: str = Field(env='REDIS_HOST')
    port: str = Field(env='REDIS_PORT')


ELASTICSEARCH = ElacticConfig()
REDISCON = RedisConfig()
POSTGRES = PostgresDsl()
SLEEP_TIME = 10

from enum import Enum
import os

class Env(Enum):
    DEV = "DEV"
    PROD = "PROD"
    TEST = "TEST"


class Config(dict):
    ENV = os.getenv('ENV', Env.DEV)
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')
    DB_URL = os.getenv('DB_URL', 'postgresql://nivo:nivo@localhost:5432/nivo')
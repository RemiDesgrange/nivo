from configparser import SafeConfigParser
from pathlib import Path
from enum import Enum
import os



class Config:
    parser: ConfigParser
    def __init__(self, ini_file: Path) -> None:
        self.parser = ConfigParser(os.environ)
        self.parser.read(ini_file)

    def __getattr__(self, name: str) -> str:
        #TODO find abetter way
        try:
            return self.parser.get(name)
        except AttributeError as e:
            raise e

class Environment(Enum):
    DEV = "DEV"
    PROD = "PROD"
    TEST = "TEST"

    def config_file_name(self):
        mapping = {
            self.DEV: "development.ini",
            self.PROD: "production.ini",
            self.TEST: "test.ini",
        }
        return mapping[self]


def load_env() -> Environment:
    env = os.getenv('ENV', 'DEV')
    try:
        return Environment(env)
    except ValueError:
        raise ValueError(f'unknown environment , need to be part of Environment Enum. Value : {env}')


def load_config() -> Config:
    env = load_env()
    return Config(env.config_file_name())


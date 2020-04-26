from enum import Enum
import os


class Env(Enum):
    DEV = "DEV"
    PROD = "PROD"
    TEST = "TEST"


class Config(dict):
    ENV = Env(os.getenv("ENV", Env.DEV))
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    DB_URL = os.getenv("DB_URL", "postgresql://nivo:nivo@localhost:5432/nivo")
    METEO_FRANCE_NIVO_BASE_URL = os.getenv(
        "METEO_FRANCE_NIVO_BASE_URL",
        "https://donneespubliques.meteofrance.fr/donnees_libres/Txt/Nivo",
    )
    METEO_FRANCE_LAST_NIVO_JS_URL = os.getenv(
        "METEO_FRANCE_LAST_NIVO_JS_URL", f"{METEO_FRANCE_NIVO_BASE_URL}/lastNivo.js"
    )
    BRA_BASE_URL = os.getenv(
        "BRA_BASE_URL", "https://donneespubliques.meteofrance.fr/donnees_libres/Pdf/BRA"
    )
    FLOWCAPT_MEASURE_URL = os.getenv(
        "FLOWCAPT_MEASURE_URL", "http://www.isaw.ch/idod/idod.php"
    )

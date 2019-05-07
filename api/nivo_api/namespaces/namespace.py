from typing import List
from flask_restplus import Namespace

from .bra import bra_api
from .nivo_meteo import nivo_meteo


def get_namespaces() -> List[Namespace]:
    return [bra_api, nivo_meteo]

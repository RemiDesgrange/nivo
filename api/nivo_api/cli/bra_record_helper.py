from datetime import datetime
from typing import Dict

from nivo_api.settings import Config


def get_last_bra_date() -> Dict[str, datetime]:
    """
    :return: a simple dict with the name of the massif as key and the date as value
    """
    today = datetime.now().date()
    request.get(Config.BRA_BASE_URL, allow_redirects=False)
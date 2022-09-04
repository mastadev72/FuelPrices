import json

import requests
from pprint import pprint

URL = 'https://api.wissol.ge/FuelPrice'
HEADERS = {
    'agent': 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G920V Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/52.0.2743.98 Mobile Safari/537.36'
}


def parse_wissol_data() -> dict:
    """
    Parse Wissol fuel prices.

    :return: dict with Wissol fuel prices
    """
    response = requests.get(URL, headers=HEADERS).text
    items = json.loads(response)

    data = {}

    for item in items:
        if item['fuelType'] != "":
            data.update({item['fuelType']: item['price']})

    data.pop('ვისოლ გაზი')

    return data


if __name__ == "__main__":
    pprint(parse_wissol_data())

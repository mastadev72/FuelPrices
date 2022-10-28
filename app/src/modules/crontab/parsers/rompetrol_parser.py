from pprint import pprint

from bs4 import BeautifulSoup

from src.modules.crontab.utils import request_url

URL = 'https://www.rompetrol.ge/#pricelist'
HEADERS = {
    'agent': 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G920V Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/52.0.2743.98 Mobile Safari/537.36'
}


def parse_rompetrol_data() -> dict:
    """
    Parse Rompetrol fuel prices.

    :return: dict with Rompetrol fuel prices
    """
    response = request_url(URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.find_all('tr')[1:]

    data = {}

    for item in items:
        data.update({item.find_all('td')[0].get_text(strip=True): item.find_all('td')[1].get_text(strip=True)})

    return data


if __name__ == "__main__":
    pprint(parse_rompetrol_data())

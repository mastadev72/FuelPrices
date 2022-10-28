from pprint import pprint

from bs4 import BeautifulSoup

from src.modules.crontab.utils import request_url

URL = 'https://www.sgp.ge/ge/price'
HEADERS = {
    'agent': 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G920V Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/52.0.2743.98 Mobile Safari/537.36'
}


def parse_socar_data() -> dict:
    """
    Parse Socar fuel prices.

    :return: dict with Socar fuel prices
    """
    response = request_url(URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    title_items = soup.find_all('th')[1:]
    price_items = soup.find_all('tr')[0].find_all('td')[1:]

    data = {}

    title_items[3].string.replace_with("ევრო რეგულარი")
    title_items[5].string.replace_with("ევრო დიზელი")

    for title, price in zip(title_items, price_items):
        data.update({title.get_text(strip=True): price.get_text(strip=True)})

    data.pop("CNG ბუნებრივი აირი")
    data.pop("ნანო რეგულარი")
    data.pop("LPG")
    return data


if __name__ == "__main__":
    pprint(parse_socar_data())

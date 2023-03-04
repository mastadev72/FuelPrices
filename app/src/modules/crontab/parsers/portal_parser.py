from pprint import pprint

from bs4 import BeautifulSoup

from src.modules.crontab.utils import request_url

URL = 'https://portal.com.ge/georgian/home'
HEADERS = {
    'agent': 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G920V Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/52.0.2743.98 Mobile Safari/537.36'
}


def parse_portal_data() -> dict:
    """
    Parse Portal.com.ge fuel prices.

    :return: dict with Portal fuel prices
    """
    response = request_url(URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.find_all('div', class_='fuel_table')

    data = {}

    for item in items:
        # Remove unnecessary tags
        tag = item.find('div', class_='color_title')
        if tag:
            tag.replace_with('')

        data.update(
            {
                item.find('div', class_='fuel_title').get_text(strip=True).replace('+', ''):
                    item.find('p', class_='old_fuel_price').get_text(strip=True)
            }
        )

    return translate_data(data)


def translate_data(data: dict) -> dict:
    """
    Translate Portal fuel names to Georgian.

    :param data: dict with Portal fuel prices
    :return: dict with translated Portal fuel prices
    """
    translated_data = {}
    translations = {
        'DIESEL': 'დიზელი',
        'EFFECT DIESEL': 'ეფექტური დიზელი',
        'EURO DIESEL': 'ევრო დიზელი',
        'EURO REGULAR': 'ევრო რეგულარი',
        'PREMIUM': 'პრემიუმი'
    }

    for key, value in data.items():
        translated_data.update(
            {
                translations[key]: value
            }
        )

    return translated_data


if __name__ == "__main__":
    pprint(parse_portal_data())

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def request_url(url: str, headers: dict = None) -> requests.Response:
    """
    Request URL.

    :param url: URL to request
    :param headers: HTTP headers
    :return: Response object
    """
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    return session.get(url, headers=headers)

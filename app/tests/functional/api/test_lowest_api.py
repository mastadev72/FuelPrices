API_URLS = [
    # Base URL
    '/api/',

    # All current prices
    '/api/lowest/',
]


def test_urls(client):
    for url in API_URLS:
        response = client.get(url)
        assert response.status_code == 200

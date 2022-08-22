APP_URLS = [
    '/',  # Home / Main page
    '/about'  # About page
]


def test_urls(client):
    for url in APP_URLS:
        response = client.get(url)
        assert response.status_code == 200


def test_price_comparison(client):
    response = client.post('/', data={
        "type_alt": "diesel"
    })

    assert response.status_code == 200

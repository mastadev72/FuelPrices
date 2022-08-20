API_URLS = [
		# All current prices
		'/api/current/',

		# Provider specific requests
		'/api/current/gulf',
		'/api/current/wissol',
		'/api/current/rompetrol',
		'/api/current/socar',
		'/api/current/lukoil'
	]


def test_urls(client):
	for url in API_URLS:
		response = client.get(url)
		assert response.status_code == 200


def test_provider_404(client):
	response = client.get(API_URLS[0] + 'provider')
	assert response.status_code == 404

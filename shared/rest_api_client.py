import requests


_API_REQUEST_TIMEOUT = 5


class RestApiClient:
    """Simple REST API client"""

    def __init__(self, base_url):
        self.base_url = base_url
        self._session = requests.Session()
        self._session.timeout = _API_REQUEST_TIMEOUT

    def create(self, data: dict, endpoint: str | None = None):
        """Sends a POST request to create a resource."""
        response = self._session.post(self._process_endpoint(endpoint), json=data)
        return response.status_code, response.json()

    def recieve(self, endpoint: str):
        """Sends a GET request to retrieve a resource"""
        response = self._session.get(self._process_endpoint(endpoint))
        return response.status_code, response.json()

    def update(self, data: dict, endpoint: str | None = None):
        """Sends a POST request to create a resource"""
        response = self._session.put(self._process_endpoint(endpoint), json=data)
        return response.status_code, response.json()

    def delete(self, endpoint: str):
        """Sends a DELETE request to remove a resource"""
        response = self._session.delete(self._process_endpoint(endpoint))
        return response.status_code, response.json()

    def perform(self, endpoint: str, params: dict | None = None):
        """Sends a command by GET request"""
        response = self._session.get(self._process_endpoint(endpoint), params=params)
        return response.status_code, response.json()

    def _process_endpoint(self, endpoint: str | None = None):
        url = f"{self.base_url}/{endpoint.lstrip('/')}" if endpoint else self.base_url
        print(f"Request {url}")
        return url

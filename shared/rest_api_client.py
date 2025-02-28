import requests
import allure

_API_REQUEST_TIMEOUT = 5


class RestApiClient:
    """Simple REST API client"""

    def __init__(self, base_url, api_key: str = None):
        self.base_url = base_url
        self._session = requests.Session()
        self._session.timeout = _API_REQUEST_TIMEOUT
        if api_key:
            self._session.headers.update({"Authorization": api_key})

    def create(self, data: dict, endpoint: str | None = None):
        """Sends a POST request to create a resource."""
        response = self._session.post(
            self._process_endpoint("POST", endpoint), json=data
        )
        return response.status_code, response.json()

    def retrieve(self, endpoint: str):
        """Sends a GET request to retrieve a resource"""
        response = self._session.get(self._process_endpoint("GET", endpoint))
        return response.status_code, response.json()

    def update(self, data: dict, endpoint: str | None = None):
        """Sends a POST request to create a resource"""
        response = self._session.put(self._process_endpoint("PUT", endpoint), json=data)
        return response.status_code, response.json()

    def delete(self, endpoint: str):
        """Sends a DELETE request to remove a resource"""
        response = self._session.delete(self._process_endpoint("DELETE", endpoint))
        return response.status_code, response.json()

    def perform(self, endpoint: str, params: dict | None = None):
        """Sends a command by GET request"""
        response = self._session.get(
            self._process_endpoint("GET", endpoint), params=params
        )
        return response.status_code, response.json()

    def _process_endpoint(
        self,
        request_type: str,
        endpoint: str | None = None,
    ):
        url = f"{self.base_url}/{endpoint.lstrip('/')}" if endpoint else self.base_url
        print(f"Send {request_type} request to {url}")
        with allure.step(f"Send {request_type} request to {url}"):
            return url

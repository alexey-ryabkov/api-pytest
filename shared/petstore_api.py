from .rest_api_client import RestApiClient

_API_BASE_URL = "https://petstore.swagger.io/v2"
OK_STATUS_CODE = 200
INVALID_DATA_SUPPLIED_STATUS_CODE = 400
NOT_FOUND_STATUS_CODE = 404
INVALID_REQUEST_STATUS_CODE = 405


def get_petstore_api(subject: str):
    """REST API Client fabric"""
    return RestApiClient(base_url=f"{_API_BASE_URL}/{subject}")

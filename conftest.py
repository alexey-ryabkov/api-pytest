import os
import sys
import platform
import importlib.metadata
import pytest
import allure

from shared.petstore_api import API_BASE_URL

ALLURE_RESULT_DIR = "allure_results"
ALLURE_ENV_FILE = f"{ALLURE_RESULT_DIR}/environment.properties"


@pytest.fixture(scope="session", autouse=True)
@allure.title("Test environment")
def test_environment():
    """Captures environment details for the Allure report."""

    def get_version(package):
        try:
            return importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            return "Not Installed"

    os.makedirs(ALLURE_RESULT_DIR, exist_ok=True)
    allure_env_data = {
        r"Test\ object": f"REST API {API_BASE_URL}",
        "OS": f"{platform.system()} {platform.release()} ({platform.architecture()[0]})",
        "Python": sys.version.split()[0],
        "pytest": pytest.__version__,
        "requests": get_version("requests"),
        "allure-pytest": get_version("allure-pytest"),
    }

    with open(ALLURE_ENV_FILE, "w", encoding="utf-8") as f:
        for key, value in allure_env_data.items():
            f.write(f"{key}={value}\n")

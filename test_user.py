import time
import pytest
from shared.petstore_api import get_petstore_api
from shared.assert_helper import (
    assert_status_code_is_ok,
    assert_status_code_is_not_found,
)


@pytest.fixture
def user_api():
    return get_petstore_api("user")


@pytest.fixture
def user_data():
    return {
        "id": 54321,
        "username": "_test_user_",
        "firstName": "Alexey",
        "lastName": "Alexeev",
        "email": "a.alexeev@example.com",
        "password": "qwerty",
        "phone": "+79999999999",
        "userStatus": 1,
    }


@pytest.fixture
def user_name(user_data):
    return user_data["username"]


def test_create_user(user_api, user_data):
    status_code, _ = user_api.create(user_data)
    assert_status_code_is_ok(status_code)
    time.sleep(5)  # waiting for the api server to apply changes


def test_recieve_user(user_api, user_name):
    status_code, user = user_api.recieve(user_name)
    assert_status_code_is_ok(status_code)
    assert user["username"] == user_name


def test_update_user(user_api, user_data, user_name):
    user_data["firstName"] = "Sebastian"
    user_data["email"] = "s.alexeev@example.com"
    status_code, _ = user_api.update(user_data, user_name)
    assert_status_code_is_ok(status_code)


def test_user_login(user_api, user_data):
    status_code, result = user_api.perform(
        "login",
        params={"username": user_data["username"], "password": user_data["password"]},
    )
    assert_status_code_is_ok(status_code)
    assert "logged in user session" in result.get("message", "")


def test_user_logout(user_api):
    status_code, result = user_api.perform("logout")
    assert_status_code_is_ok(status_code)
    assert "ok" in result.get("message", "").lower()


def test_delete_user(user_api, user_name):
    status_code, _ = user_api.delete(user_name)
    assert_status_code_is_ok(status_code)
    time.sleep(20)  # waiting for the api server to apply the request
    status_code, _ = user_api.recieve(user_name)
    assert_status_code_is_not_found(status_code)

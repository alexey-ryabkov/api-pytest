import pytest
import allure

from shared.petstore_api import get_petstore_api
from shared.assert_helper import (
    assert_status_code_is_ok,
    assert_status_code_is_not_found,
)
from shared.utils import (
    allure_test_desc_n_input_data,
    allure_annotation_fabric,
)


API_ENTITY_NAME = "user"
allure_annotation = allure_annotation_fabric(
    f"Test {API_ENTITY_NAME} entity in Petstore API"
)


@pytest.fixture
@allure.title(f"REST API client instance for {API_ENTITY_NAME} entity")
def user_api():
    return get_petstore_api(API_ENTITY_NAME)


@pytest.fixture
@allure.title("User data")
def user_data():
    return {
        "id": 633181,
        "username": "_test__user_",
        "firstName": "Alexey",
        "lastName": "Alexeev",
        "email": "a.alexeev@example.com",
        "password": "qwerty",
        "phone": "+79999999999",
        "userStatus": 1,
    }


@pytest.fixture
@allure.title("User name")
def user_name(user_data):
    return user_data["username"]


@allure_annotation("Create a user")
def test_create_user(user_api, user_data):
    allure_test_desc_n_input_data(
        "Creates a new user and verifies the response contains correct data.",
        user_data,
        "User data",
    )
    with allure.step("Send request to create a user"):
        status_code, _ = user_api.create(user_data)
    assert_status_code_is_ok(status_code)


@allure_annotation(
    "Retrieve an existing user",
    "This test verifies that an existing user can be retrieved by use name.",
)
@pytest.mark.flaky(reruns=5, reruns_delay=1)
def test_retrieve_user(user_api, user_name):
    with allure.step("Send request to retrieve a user"):
        status_code, user = user_api.retrieve(user_name)
    assert_status_code_is_ok(status_code)
    with allure.step("Verify user names match"):
        assert user["username"] == user_name


@allure_annotation("Log in a user")
def test_user_login(user_api, user_data):
    login_params = {
        "username": user_data["username"],
        "password": user_data["password"],
    }
    allure_test_desc_n_input_data(
        "This test verifies that the user can log in.", login_params, "Log in params"
    )
    with allure.step("Send request to user log in"):
        status_code, result = user_api.perform(
            "login",
            params=login_params,
        )
    assert_status_code_is_ok(status_code)
    with allure.step("Verify response message is appropriate"):
        assert "logged in user session" in result.get("message", "")


@allure_annotation("Update a user")
def test_update_user(user_api, user_data, user_name):
    user_data["firstName"] = "Sebastian"
    user_data["email"] = "s.alexeev@example.com"
    allure_test_desc_n_input_data(
        "This test verifies that the user can be updated.", user_data, "User data"
    )
    with allure.step("Send request to update a user name and email"):
        status_code, _ = user_api.update(user_data, user_name)
    assert_status_code_is_ok(status_code)


@allure_annotation("Log out a user")
def test_user_logout(user_api):
    with allure.step("Send request to user log out"):
        status_code, result = user_api.perform("logout")
    assert_status_code_is_ok(status_code)
    with allure.step("Verify response message is appropriate"):
        assert "ok" in result.get("message", "").lower()


@allure_annotation(
    "Delete a user",
    "This test verifies that a user can be deleted and is no longer retrievable.",
)
@pytest.mark.flaky(reruns=5, reruns_delay=1)
def test_delete_user(user_api, user_name):
    with allure.step("Send request to delete a user"):
        status_code, _ = user_api.delete(user_name)
    assert_status_code_is_ok(status_code)
    with allure.step("Send request to get a user"):
        status_code1, _ = user_api.retrieve(user_name)
    assert_status_code_is_not_found(status_code1)

import pytest
import requests

API_BASE_URL = "https://petstore.swagger.io/v2/user"


@pytest.fixture
def create_user():
    user_data = {
        "id": 1001,
        "username": "testuser",
        "firstName": "Alexey",
        "lastName": "Alexeev",
        "email": "a.alexeev@example.com",
        "password": "123456",
        "phone": "+79999999999",
        "userStatus": 1,
    }
    response = requests.post(API_BASE_URL, json=user_data)
    assert response.status_code == 200
    return user_data


@pytest.fixture
def user_name(create_user):
    return create_user["username"]


def test_create_user(create_user):
    response = requests.get(f"{API_BASE_URL}/{create_user['username']}")
    assert response.status_code == 200
    user = response.json()
    assert user["username"] == create_user["username"]
    assert user["email"] == create_user["email"]


def test_get_user(user_name):
    response = requests.get(f"{API_BASE_URL}/{user_name}")
    assert response.status_code == 200
    user = response.json()
    assert user["username"] == user_name


def test_update_user(user_name):
    updated_data = {
        "id": 1001,
        "username": "testuser",
        "firstName": "Sebastian",
        "lastName": "Alexeev",
        "email": "s.alexeev@example.com",
        "password": "123456",
        "phone": "+79999999999",
        "userStatus": 1,
    }
    response = requests.put(f"{API_BASE_URL}/{user_name}", json=updated_data)
    assert response.status_code == 200
    user = response.json()
    assert user["firstName"] == "Sebastian"
    assert user["email"] == "s.alexeev@example.com"


def test_user_login(user_name):
    response = requests.get(
        f"{API_BASE_URL}/login",
        params={"username": user_name, "password": "securepass"},
    )
    assert response.status_code == 200
    assert "logged in user session" in response.json().get("message", "")


def test_user_logout():
    response = requests.get(f"{API_BASE_URL}/logout")
    assert response.status_code == 200
    assert "ok" in response.json().get("message", "").lower()


def test_delete_user(user_name):
    response = requests.delete(f"{API_BASE_URL}/{user_name}")
    assert response.status_code == 200
    response = requests.get(f"{API_BASE_URL}/{user_name}")
    assert response.status_code == 404

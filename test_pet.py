import pytest
import requests

API_BASE_URL = "https://petstore.swagger.io/v2/pet"


@pytest.fixture
def create_pet():
    pet_data = {
        "id": 12345,
        "name": "Fluffy",
        "category": {"id": 1, "name": "Cats"},
        "status": "available",
    }
    response = requests.post(API_BASE_URL, json=pet_data)
    assert response.status_code == 200
    return pet_data


@pytest.fixture
def pet_id(create_pet):
    return create_pet["id"]


def test_create_pet(create_pet):
    response = requests.get(f"{API_BASE_URL}/{create_pet['id']}")
    assert response.status_code == 200
    pet = response.json()
    assert pet["name"] == create_pet["name"]
    assert pet["category"]["name"] == create_pet["category"]["name"]
    assert pet["status"] == create_pet["status"]


def test_update_pet(pet_id):
    updated_data = {
        "id": pet_id,
        "name": "Fluffy updated",
        "category": {"id": 1, "name": "Cats"},
        "status": "available",
    }
    response = requests.put(f"{API_BASE_URL}/{pet_id}", json=updated_data)
    assert response.status_code == 200
    pet = response.json()
    assert pet["name"] == "Fluffy updated"


def test_update_pet_status(pet_id):
    updated_data = {"id": pet_id, "status": "sold"}
    response = requests.put(f"{API_BASE_URL}/{pet_id}", json=updated_data)
    assert response.status_code == 200
    pet = response.json()
    assert pet["status"] == "sold"


def test_get_pet(pet_id):
    response = requests.get(f"{API_BASE_URL}/{pet_id}")
    assert response.status_code == 200
    pet = response.json()
    assert pet["id"] == pet_id


def test_delete_pet(pet_id):
    response = requests.delete(f"{API_BASE_URL}/{pet_id}")
    assert response.status_code == 200
    response = requests.get(f"{API_BASE_URL}/{pet_id}")
    assert response.status_code == 404

import time
import pytest
from shared.petstore_api import get_petstore_api
from shared.assert_helper import (
    assert_status_code_is_ok,
    assert_status_code_is_not_found,
    assert_fields_match,
)


@pytest.fixture
def pet_api():
    return get_petstore_api("pet")


@pytest.fixture
def pet_data():
    return {
        "id": 12345,
        "name": "Fluffy",
        "category": {"id": 1, "name": "Cats"},
        "status": "available",
    }


@pytest.fixture
def pet_id(pet_data):
    return pet_data["id"]


def test_create_pet(pet_api, pet_data):
    status_code, pet = pet_api.create(pet_data)
    assert_status_code_is_ok(status_code)
    assert_fields_match(pet, pet_data, ["name", ["category", "name"], "status"])
    time.sleep(5)  # waiting for the api server to apply changes


def test_recieve_pet(pet_api, pet_id):
    status_code, pet = pet_api.recieve(pet_id)
    assert_status_code_is_ok(status_code)
    assert pet["id"] == pet_id


def test_update_pet(pet_api, pet_data):
    pet_data["name"] = "Snowball"
    status_code, pet = pet_api.update(pet_data)
    assert_status_code_is_ok(status_code)
    assert_fields_match(pet, pet_data, ["name"])


def test_update_pet_status(pet_api, pet_id):
    update_data = {"id": pet_id, "status": "sold"}
    status_code, pet = pet_api.update(update_data)
    assert_status_code_is_ok(status_code)
    assert_fields_match(pet, update_data, ["status"])


def test_delete_pet(pet_api, pet_id):
    status_code, _ = pet_api.delete(pet_id)
    assert_status_code_is_ok(status_code)
    time.sleep(5)  # waiting for the api server to apply the request
    status_code, _ = pet_api.recieve(pet_id)
    assert_status_code_is_not_found(status_code)

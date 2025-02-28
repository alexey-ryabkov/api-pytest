import pytest
import allure

from shared.petstore_api import get_petstore_api
from shared.assert_helper import (
    assert_status_code_is_ok,
    assert_status_code_is_not_found,
    assert_fields_match,
)
from shared.utils import (
    allure_test_desc_n_input_data,
    allure_annotation_fabric,
    wait_server_apply_changes,
)


API_ENTITY_NAME = "pet"
allure_annotation = allure_annotation_fabric(
    f"Test {API_ENTITY_NAME} entity in Petstore API"
)


@pytest.fixture
@allure.title(f"REST API client instance for {API_ENTITY_NAME} entity")
def pet_api():
    return get_petstore_api(API_ENTITY_NAME)


@pytest.fixture
@allure.title("Pet data")
def pet_data():
    data = {
        "id": 12345,
        "name": "Fluffy",
        "category": {"id": 1, "name": "Cats"},
        "status": "available",
    }
    return data


@pytest.fixture
@allure.title("Pet ID")
def pet_id(pet_data):
    return pet_data["id"]


@allure_annotation("Create a pet")
def test_create_pet(pet_api, pet_data):
    allure_test_desc_n_input_data(
        "Creates a new pet and verifies the response contains correct data.",
        pet_data,
        "Pet data",
    )
    with allure.step("Send request to create a pet"):
        status_code, pet = pet_api.create(pet_data)
    assert_status_code_is_ok(status_code)
    assert_fields_match(pet, pet_data, ["name", ["category", "name"], "status"])
    wait_server_apply_changes(5)


@allure_annotation(
    "Retrieve an existing pet",
    "This test verifies that an existing pet can be retrieved by ID.",
)
def test_recieve_pet(pet_api, pet_id):
    with allure.step("Send request to recieve a pet"):
        status_code, pet = pet_api.recieve(str(pet_id))
    assert_status_code_is_ok(status_code)
    with allure.step("Verify a pet IDs match"):
        assert pet["id"] == pet_id


@allure_annotation("Update a pet")
def test_update_pet(pet_api, pet_data):
    pet_data["name"] = "Snowball"
    allure_test_desc_n_input_data(
        "This test verifies that the pet's name can be updated.", pet_data, "Pet data"
    )
    with allure.step("Send request to update a pet name"):
        status_code, pet = pet_api.update(pet_data)
    assert_status_code_is_ok(status_code)
    assert_fields_match(pet, pet_data, ["name"])


@allure_annotation(
    "Update a pet status", "This test verifies that the pet's status can be updated."
)
def test_update_pet_status(pet_api, pet_id):
    update_data = {"id": pet_id, "status": "sold"}
    with allure.step("Send request to update a pet status"):
        status_code, pet = pet_api.update(update_data)
    assert_status_code_is_ok(status_code)
    assert_fields_match(pet, update_data, ["status"])


@allure_annotation(
    "Delete a pet",
    "This test verifies that a pet can be deleted and is no longer retrievable.",
)
def test_delete_pet(pet_api, pet_id):
    with allure.step("Send request to delete a pet"):
        status_code, _ = pet_api.delete(str(pet_id))
    assert_status_code_is_ok(status_code)
    wait_server_apply_changes(5)
    with allure.step("Send request to get a pet"):
        status_code, _ = pet_api.recieve(str(pet_id))
    assert_status_code_is_not_found(status_code)

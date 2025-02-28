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


API_ENTITY_NAME = "store"
allure_annotation = allure_annotation_fabric(
    f"Test {API_ENTITY_NAME} entity in Petstore API"
)


@pytest.fixture
@allure.title(f"REST API client instance for {API_ENTITY_NAME} entity")
def store_api():
    return get_petstore_api(API_ENTITY_NAME)


@pytest.fixture
@allure.title("Order data")
def order_data():
    return {
        "id": 314314,
        "petId": 12345,
        "quantity": 2,
        "shipDate": "2025-02-25T15:00:00.000Z",
        "status": "placed",
        "complete": False,
    }


@pytest.fixture
@allure.title("Order ID")
def order_id(order_data):
    return order_data["id"]


@allure_annotation("Create an order")
def test_create_order(store_api, order_data):
    allure_test_desc_n_input_data(
        "Creates a new order and verifies the response contains correct data.",
        order_data,
        "Order data",
    )
    with allure.step("Send request to create an order"):
        status_code, order = store_api.create(order_data, "order")
    assert_status_code_is_ok(status_code)
    assert_fields_match(order, order_data, ["id", "status"])
    wait_server_apply_changes(10)


@allure_annotation(
    "Retrieve an existing order",
    "This test verifies that an existing order can be retrieved by ID.",
)
def test_recieve_order(store_api, order_id):
    with allure.step("Send request to recieve an order"):
        status_code, order = store_api.recieve(f"order/{order_id}")
    assert_status_code_is_ok(status_code)
    with allure.step("Verify an order IDs match"):
        assert order["id"] == order_id


@allure_annotation(
    "Retrieve an order status",
    "This test verifies that an order status can be retrieved and has appropriate value.",
)
def test_order_status(store_api, order_id):
    _, order = store_api.recieve(f"order/{order_id}")
    print(order)
    with allure.step("Verify an order status has appropriate value"):
        assert order["status"] in ["placed", "sold", "available"]


@allure_annotation(
    "Delete an order",
    "This test verifies that an order can be deleted and is no longer retrievable.",
)
def test_delete_order(store_api, order_id):
    with allure.step("Send request to delete an order"):
        status_code, _ = store_api.delete(f"order/{order_id}")
    assert_status_code_is_ok(status_code)
    wait_server_apply_changes(20)
    with allure.step("Send request to get an order"):
        status_code, _ = store_api.recieve(f"order/{order_id}")
    assert_status_code_is_not_found(status_code)


@allure_annotation(
    "Retrieve inventory stats",
    "This test verifies that inventory stats can be retrieved.",
)
def test_get_inventory(store_api):
    with allure.step("Send request to retrieve inventory stats"):
        status_code, inventory = store_api.recieve("inventory")
    assert_status_code_is_ok(status_code)
    assert isinstance(inventory, dict)
    with allure.step("Verify an inventory has stats for sold n available"):
        assert "sold" in inventory or "available" in inventory

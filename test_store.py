import time
import pytest
from shared.petstore_api import get_petstore_api
from shared.assert_helper import (
    assert_status_code_is_ok,
    assert_status_code_is_not_found,
    assert_fields_match,
)


@pytest.fixture
def store_api():
    return get_petstore_api("store")


@pytest.fixture
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
def order_id(order_data):
    return order_data["id"]


def test_create_order(store_api, order_data):
    status_code, order = store_api.create(order_data, "order")
    assert_status_code_is_ok(status_code)
    assert_fields_match(order, order_data, ["id", "status"])
    time.sleep(5)  # waiting for the api server to apply changes


def test_recieve_order(store_api, order_id):
    status_code, order = store_api.recieve(f"order/{order_id}")
    assert_status_code_is_ok(status_code)
    assert order["id"] == order_id


def test_order_status(store_api, order_id):
    _, order = store_api.recieve(f"order/{order_id}")
    print(order)
    assert order["status"] in ["placed", "approved", "delivered"]


def test_delete_order(store_api, order_id):
    status_code, _ = store_api.delete(f"order/{order_id}")
    assert_status_code_is_ok(status_code)
    time.sleep(5)  # waiting for the api server to apply the request
    status_code, _ = store_api.recieve(f"order/{order_id}")
    assert_status_code_is_not_found(status_code)


def test_get_inventory(store_api):
    status_code, inventory = store_api.recieve("inventory")
    assert_status_code_is_ok(status_code)
    assert isinstance(inventory, dict)
    assert "sold" in inventory or "available" in inventory

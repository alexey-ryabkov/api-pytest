import pytest
import requests

API_BASE_URL = "https://petstore.swagger.io/v2/store"


@pytest.fixture
def create_order():
    order_data = {
        "id": 5001,
        "petId": 1001,
        "quantity": 2,
        "shipDate": "2025-02-25T15:00:00.000Z",
        "status": "placed",
        "complete": False,
    }
    response = requests.post(f"{API_BASE_URL}/order", json=order_data)
    assert response.status_code == 200
    return order_data


@pytest.fixture
def order_id(create_order):
    return create_order["id"]


def test_create_order(create_order):
    response = requests.get(f"{API_BASE_URL}/order/{create_order['id']}")
    assert response.status_code == 200
    order = response.json()
    assert order["id"] == create_order["id"]
    assert order["status"] == create_order["status"]


def test_get_order(order_id):
    response = requests.get(f"{API_BASE_URL}/order/{order_id}")
    assert response.status_code == 200
    order = response.json()
    assert order["id"] == order_id


def test_delete_order(order_id):
    response = requests.delete(f"{API_BASE_URL}/order/{order_id}")
    assert response.status_code == 200
    response = requests.get(f"{API_BASE_URL}/order/{order_id}")
    assert response.status_code == 404


def test_order_status(order_id):
    response = requests.get(f"{API_BASE_URL}/order/{order_id}")
    assert response.status_code == 200
    order = response.json()
    assert order["status"] in ["placed", "approved", "delivered"]


def test_get_inventory():
    response = requests.get(f"{API_BASE_URL}/inventory")
    assert response.status_code == 200
    inventory = response.json()
    assert isinstance(inventory, dict)
    assert "sold" in inventory or "available" in inventory

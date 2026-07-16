from pathlib import Path
import shutil


def setup_function():
    shutil.rmtree("storage/invoices", ignore_errors=True)
    shutil.rmtree("storage/notifications", ignore_errors=True)


def test_checkout_creates_order_and_background_files(client, auth_headers):
    client.post(
        "/cart",
        json={"product_id": 1, "quantity": 2},
        headers=auth_headers
    )

    response = client.post("/orders", headers=auth_headers)

    assert response.status_code == 201
    data = response.json()

    assert data["status"] == "PENDING"
    assert len(data["items"]) == 1
    assert data["items"][0]["quantity"] == 2
    assert data["items"][0]["product"]["id"] == 1

    order_id = data["id"]

    invoice_file = Path(f"storage/invoices/order_{order_id}_invoice.json")
    assert invoice_file.exists()

    notification_files = list(
        Path("storage/notifications").glob(
            f"order_{order_id}_order_created_*.json"
        )
    )
    assert len(notification_files) == 1


def test_get_orders_returns_user_orders(client, auth_headers):
    client.post(
        "/cart",
        json={"product_id": 1, "quantity": 1},
        headers=auth_headers
    )
    client.post("/orders", headers=auth_headers)

    response = client.get("/orders", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["status"] == "PENDING"
    assert len(data[0]["items"]) == 1


def test_status_update_creates_notification_file(client, auth_headers):
    client.post(
        "/cart",
        json={"product_id": 1, "quantity": 1},
        headers=auth_headers
    )

    create_response = client.post("/orders", headers=auth_headers)
    order_id = create_response.json()["id"]

    response = client.patch(
        f"/orders/{order_id}/status",
        json={"status": "PAID"},
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "PAID"

    notification_files = list(
        Path("storage/notifications").glob(
            f"order_{order_id}_order_status_updated_*.json"
        )
    )
    assert len(notification_files) == 1


def test_cancel_order_creates_notification_file(client, auth_headers):
    client.post(
        "/cart",
        json={"product_id": 1, "quantity": 1},
        headers=auth_headers
    )

    create_response = client.post("/orders", headers=auth_headers)
    order_id = create_response.json()["id"]

    response = client.post(
        f"/orders/{order_id}/cancel",
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "CANCELLED"

    notification_files = list(
        Path("storage/notifications").glob(
            f"order_{order_id}_order_cancelled_*.json"
        )
    )
    assert len(notification_files) == 1
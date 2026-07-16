def test_create_mock_payment(client, auth_headers):
    client.post(
        "/cart",
        json={"product_id": 1, "quantity": 1},
        headers=auth_headers
    )
    order_response = client.post("/orders", headers=auth_headers)
    order_id = order_response.json()["id"]

    response = client.post(
        "/payments",
        json={"order_id": order_id},
        headers=auth_headers
    )

    assert response.status_code == 201
    data = response.json()
    assert data["order_id"] == order_id
    assert data["status"] == "PENDING"
    assert data["provider"] == "mock"


def test_webhook_marks_payment_paid_and_updates_order(client, auth_headers):
    client.post(
        "/cart",
        json={"product_id": 1, "quantity": 1},
        headers=auth_headers
    )
    order_response = client.post("/orders", headers=auth_headers)
    order_id = order_response.json()["id"]

    payment_response = client.post(
        "/payments",
        json={"order_id": order_id},
        headers=auth_headers
    )
    payment_id = payment_response.json()["id"]

    webhook_response = client.post(
        "/webhooks",
        json={"payment_id": payment_id, "status": "PAID"}
    )

    assert webhook_response.status_code == 200
    payment_data = webhook_response.json()
    assert payment_data["status"] == "PAID"

    order_check = client.get(f"/orders/{order_id}", headers=auth_headers)
    assert order_check.status_code == 200
    assert order_check.json()["status"] == "PAID"


def test_webhook_marks_payment_failed_without_paying_order(client, auth_headers):
    client.post(
        "/cart",
        json={"product_id": 1, "quantity": 1},
        headers=auth_headers
    )
    order_response = client.post("/orders", headers=auth_headers)
    order_id = order_response.json()["id"]

    payment_response = client.post(
        "/payments",
        json={"order_id": order_id},
        headers=auth_headers
    )
    payment_id = payment_response.json()["id"]

    webhook_response = client.post(
        "/webhooks",
        json={"payment_id": payment_id, "status": "FAILED"}
    )

    assert webhook_response.status_code == 200
    payment_data = webhook_response.json()
    assert payment_data["status"] == "FAILED"

    order_check = client.get(f"/orders/{order_id}", headers=auth_headers)
    assert order_check.status_code == 200
    assert order_check.json()["status"] == "PENDING"
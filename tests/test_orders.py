def test_checkout_creates_order(client, auth_headers):
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
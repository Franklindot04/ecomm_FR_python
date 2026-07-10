def test_add_to_cart(client, auth_headers):
    response = client.post(
        "/cart",
        json={"product_id": 1, "quantity": 2},
        headers=auth_headers
    )

    assert response.status_code == 201
    data = response.json()
    assert data["quantity"] == 2
    assert data["product"]["id"] == 1
    assert data["product"]["name"] == "Keyboard"


def test_get_cart_items(client, auth_headers):
    client.post(
        "/cart",
        json={"product_id": 1, "quantity": 2},
        headers=auth_headers
    )

    response = client.get("/cart", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["quantity"] == 2
    assert data[0]["product"]["id"] == 1
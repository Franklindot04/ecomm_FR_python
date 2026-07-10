def test_get_all_products(client):
    response = client.get("/products")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2


def test_get_single_product(client):
    response = client.get("/products/1")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Keyboard"
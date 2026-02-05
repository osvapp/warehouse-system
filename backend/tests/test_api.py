from app import create_app, db



def test_health_check():
    app = create_app(
        {"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"}
    )

    with app.app_context():
        db.create_all()

    client = app.test_client()
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json == {"status": "ok"}


def test_create_and_list_items():
    app = create_app(
        {"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"}
    )

    with app.app_context():
        db.create_all()

    client = app.test_client()

    create_response = client.post(
        "/api/items",
        json={"sku": "SKU-001", "name": "Keyboard", "quantity": 10, "location": "A1"},
    )
    assert create_response.status_code == 201

    list_response = client.get("/api/items")
    assert list_response.status_code == 200
    assert len(list_response.json) == 1
    assert list_response.json[0]["sku"] == "SKU-001"

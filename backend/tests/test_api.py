from app import create_app, db


def _make_app():
    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})
    with app.app_context():
        db.create_all()
    return app


def test_auth_register_and_login():
    app = _make_app()
    client = app.test_client()

    register = client.post("/api/auth/register", json={"username": "admin", "password": "123456"})
    assert register.status_code == 201

    login = client.post("/api/auth/login", json={"username": "admin", "password": "123456"})
    assert login.status_code == 200
    assert "token" in login.json


def test_inventory_inbound_outbound_and_alerts():
    app = _make_app()
    client = app.test_client()

    created = client.post(
        "/api/items",
        json={"sku": "SKU-001", "name": "Keyboard", "quantity": 5, "min_stock": 3},
    )
    assert created.status_code == 201
    item_id = created.json["id"]

    inbound = client.post("/api/inbound-orders", json={"item_id": item_id, "quantity": 10})
    assert inbound.status_code == 201

    outbound = client.post("/api/outbound-orders", json={"item_id": item_id, "quantity": 12})
    assert outbound.status_code == 201

    alerts = client.post("/api/alerts/generate")
    assert alerts.status_code == 200


def test_bill_generation():
    app = _make_app()
    client = app.test_client()

    create_bill = client.post(
        "/api/bills",
        json={"bill_no": "BILL-001", "bill_type": "receivable", "amount": 100.0},
    )
    assert create_bill.status_code == 201

    auto_bill = client.post(
        "/api/bills/generate",
        json={"source": "outbound", "reference_id": 1, "amount": 88.8},
    )
    assert auto_bill.status_code == 201

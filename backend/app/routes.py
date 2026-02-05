from datetime import datetime

from flask import Blueprint, jsonify, request

from . import db
from .models import (
    Bill,
    Customer,
    Employee,
    InboundOrder,
    InventoryAlert,
    Item,
    OutboundOrder,
    Permission,
    Role,
    Supplier,
    User,
    Warehouse,
    WarehouseStaff,
)


inventory_bp = Blueprint("inventory", __name__)


def _json_error(message: str, status: int = 400):
    return jsonify({"error": message}), status


def _crud_list(model):
    rows = model.query.order_by(model.id.desc()).all()
    return jsonify([row.to_dict() for row in rows])


def _check_inventory_alert(item: Item) -> None:
    if item.quantity <= item.min_stock:
        alert = InventoryAlert(
            item_id=item.id,
            current_quantity=item.quantity,
            threshold=item.min_stock,
            status="open",
        )
        db.session.add(alert)


@inventory_bp.post("/auth/register")
def register():
    payload = request.get_json(silent=True) or {}
    username = payload.get("username", "").strip()
    password = payload.get("password", "")
    if not username or len(password) < 6:
        return _json_error("username required and password length >= 6")
    if User.query.filter_by(username=username).first():
        return _json_error("username already exists", 409)
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201


@inventory_bp.post("/auth/login")
def login():
    payload = request.get_json(silent=True) or {}
    user = User.query.filter_by(username=payload.get("username", "").strip()).first()
    if not user or not user.check_password(payload.get("password", "")):
        return _json_error("invalid credentials", 401)
    token = f"token-{user.id}-{int(datetime.utcnow().timestamp())}"
    return jsonify({"token": token, "user": user.to_dict()})


@inventory_bp.get("/warehouses")
def list_warehouses():
    return _crud_list(Warehouse)


@inventory_bp.post("/warehouses")
def create_warehouse():
    payload = request.get_json(silent=True) or {}
    code = payload.get("code", "").strip()
    name = payload.get("name", "").strip()
    if not code or not name:
        return _json_error("code and name are required")
    if Warehouse.query.filter_by(code=code).first():
        return _json_error("warehouse code already exists", 409)
    obj = Warehouse(code=code, name=name, location=payload.get("location"))
    db.session.add(obj)
    db.session.commit()
    return jsonify(obj.to_dict()), 201


@inventory_bp.get("/warehouse-staff")
def list_warehouse_staff():
    return _crud_list(WarehouseStaff)


@inventory_bp.post("/warehouse-staff")
def create_warehouse_staff():
    payload = request.get_json(silent=True) or {}
    if not payload.get("name"):
        return _json_error("name is required")
    obj = WarehouseStaff(
        name=payload["name"],
        phone=payload.get("phone"),
        warehouse_id=payload.get("warehouse_id"),
    )
    db.session.add(obj)
    db.session.commit()
    return jsonify(obj.to_dict()), 201


@inventory_bp.get("/items")
def list_items():
    return _crud_list(Item)


@inventory_bp.post("/items")
def create_item():
    payload = request.get_json(silent=True) or {}
    for field in ["sku", "name", "quantity"]:
        if field not in payload:
            return _json_error(f"Missing required field: {field}")
    if not isinstance(payload["quantity"], int) or payload["quantity"] < 0:
        return _json_error("quantity must be a non-negative integer")
    if Item.query.filter_by(sku=payload["sku"]).first():
        return _json_error("sku already exists", 409)
    item = Item(
        sku=payload["sku"],
        name=payload["name"],
        quantity=payload["quantity"],
        location=payload.get("location"),
        min_stock=max(0, int(payload.get("min_stock", 0))),
        warehouse_id=payload.get("warehouse_id"),
    )
    _check_inventory_alert(item)
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201


@inventory_bp.put("/items/<int:item_id>")
def update_item(item_id: int):
    item = Item.query.get_or_404(item_id)
    payload = request.get_json(silent=True) or {}
    for field in ["name", "sku", "quantity", "location", "min_stock", "warehouse_id"]:
        if field in payload:
            setattr(item, field, payload[field])
    if item.quantity < 0:
        return _json_error("quantity must be non-negative")
    _check_inventory_alert(item)
    db.session.commit()
    return jsonify(item.to_dict())


@inventory_bp.delete("/items/<int:item_id>")
def delete_item(item_id: int):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return "", 204


@inventory_bp.get("/suppliers")
def list_suppliers():
    return _crud_list(Supplier)


@inventory_bp.post("/suppliers")
def create_supplier():
    payload = request.get_json(silent=True) or {}
    if not payload.get("name"):
        return _json_error("name is required")
    obj = Supplier(name=payload["name"], contact=payload.get("contact"), phone=payload.get("phone"))
    db.session.add(obj)
    db.session.commit()
    return jsonify(obj.to_dict()), 201


@inventory_bp.get("/customers")
def list_customers():
    return _crud_list(Customer)


@inventory_bp.post("/customers")
def create_customer():
    payload = request.get_json(silent=True) or {}
    if not payload.get("name"):
        return _json_error("name is required")
    obj = Customer(name=payload["name"], contact=payload.get("contact"), phone=payload.get("phone"))
    db.session.add(obj)
    db.session.commit()
    return jsonify(obj.to_dict()), 201


@inventory_bp.get("/inbound-orders")
def list_inbound_orders():
    return _crud_list(InboundOrder)


@inventory_bp.post("/inbound-orders")
def create_inbound_order():
    payload = request.get_json(silent=True) or {}
    item_id = payload.get("item_id")
    quantity = payload.get("quantity")
    if not item_id or not isinstance(quantity, int) or quantity <= 0:
        return _json_error("item_id and positive quantity are required")
    item = Item.query.get_or_404(item_id)
    item.quantity += quantity
    _check_inventory_alert(item)
    order = InboundOrder(
        item_id=item_id,
        supplier_id=payload.get("supplier_id"),
        quantity=quantity,
        note=payload.get("note"),
    )
    db.session.add(order)
    db.session.commit()
    return jsonify(order.to_dict()), 201


@inventory_bp.get("/outbound-orders")
def list_outbound_orders():
    return _crud_list(OutboundOrder)


@inventory_bp.post("/outbound-orders")
def create_outbound_order():
    payload = request.get_json(silent=True) or {}
    item_id = payload.get("item_id")
    quantity = payload.get("quantity")
    if not item_id or not isinstance(quantity, int) or quantity <= 0:
        return _json_error("item_id and positive quantity are required")
    item = Item.query.get_or_404(item_id)
    if item.quantity < quantity:
        return _json_error("insufficient stock", 400)
    item.quantity -= quantity
    _check_inventory_alert(item)
    order = OutboundOrder(
        item_id=item_id,
        customer_id=payload.get("customer_id"),
        quantity=quantity,
        note=payload.get("note"),
    )
    db.session.add(order)
    db.session.commit()
    return jsonify(order.to_dict()), 201


@inventory_bp.get("/alerts")
def list_alerts():
    return _crud_list(InventoryAlert)


@inventory_bp.post("/alerts/generate")
def generate_alerts():
    created = 0
    for item in Item.query.all():
        if item.quantity <= item.min_stock:
            alert = InventoryAlert(
                item_id=item.id,
                current_quantity=item.quantity,
                threshold=item.min_stock,
                status="open",
            )
            db.session.add(alert)
            created += 1
    db.session.commit()
    return jsonify({"created": created})


@inventory_bp.get("/bills")
def list_bills():
    return _crud_list(Bill)


@inventory_bp.post("/bills")
def create_bill():
    payload = request.get_json(silent=True) or {}
    for field in ["bill_no", "bill_type", "amount"]:
        if field not in payload:
            return _json_error(f"missing field {field}")
    bill = Bill(
        bill_no=payload["bill_no"],
        bill_type=payload["bill_type"],
        amount=float(payload["amount"]),
        reference_type=payload.get("reference_type"),
        reference_id=payload.get("reference_id"),
        status=payload.get("status", "draft"),
    )
    db.session.add(bill)
    db.session.commit()
    return jsonify(bill.to_dict()), 201


@inventory_bp.post("/bills/generate")
def generate_bill():
    payload = request.get_json(silent=True) or {}
    source = payload.get("source")
    reference_id = payload.get("reference_id")
    amount = float(payload.get("amount", 0))
    if source not in {"inbound", "outbound"}:
        return _json_error("source must be inbound or outbound")
    bill = Bill(
        bill_no=f"BILL-{int(datetime.utcnow().timestamp())}",
        bill_type="payable" if source == "inbound" else "receivable",
        reference_type=source,
        reference_id=reference_id,
        amount=amount,
        status="generated",
    )
    db.session.add(bill)
    db.session.commit()
    return jsonify(bill.to_dict()), 201


@inventory_bp.get("/employees")
def list_employees():
    return _crud_list(Employee)


@inventory_bp.post("/employees")
def create_employee():
    payload = request.get_json(silent=True) or {}
    if not payload.get("name") or not payload.get("email"):
        return _json_error("name and email are required")
    employee = Employee(
        name=payload["name"], email=payload["email"], position=payload.get("position")
    )
    db.session.add(employee)
    db.session.commit()
    return jsonify(employee.to_dict()), 201


@inventory_bp.get("/permissions")
def list_permissions():
    return _crud_list(Permission)


@inventory_bp.post("/permissions")
def create_permission():
    payload = request.get_json(silent=True) or {}
    if not payload.get("code") or not payload.get("name"):
        return _json_error("code and name are required")
    permission = Permission(code=payload["code"], name=payload["name"])
    db.session.add(permission)
    db.session.commit()
    return jsonify(permission.to_dict()), 201


@inventory_bp.get("/roles")
def list_roles():
    return _crud_list(Role)


@inventory_bp.post("/roles")
def create_role():
    payload = request.get_json(silent=True) or {}
    if not payload.get("code") or not payload.get("name"):
        return _json_error("code and name are required")
    role = Role(code=payload["code"], name=payload["name"])
    permission_ids = payload.get("permission_ids", [])
    if permission_ids:
        role.permissions = Permission.query.filter(Permission.id.in_(permission_ids)).all()
    db.session.add(role)
    db.session.commit()
    return jsonify(role.to_dict()), 201


@inventory_bp.post("/roles/<int:role_id>/permissions")
def assign_permissions(role_id: int):
    role = Role.query.get_or_404(role_id)
    payload = request.get_json(silent=True) or {}
    permission_ids = payload.get("permission_ids", [])
    role.permissions = Permission.query.filter(Permission.id.in_(permission_ids)).all()
    db.session.commit()
    return jsonify(role.to_dict())

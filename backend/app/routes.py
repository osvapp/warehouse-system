from flask import Blueprint, jsonify, request

from . import db
from .models import Item


inventory_bp = Blueprint("inventory", __name__)


def _validate_payload(payload: dict) -> tuple[bool, str | None]:
    required = ["sku", "name", "quantity"]
    for key in required:
        if key not in payload:
            return False, f"Missing required field: {key}"

    if not isinstance(payload["quantity"], int) or payload["quantity"] < 0:
        return False, "quantity must be a non-negative integer"

    return True, None


@inventory_bp.get("/items")
def list_items():
    items = Item.query.order_by(Item.id.desc()).all()
    return jsonify([item.to_dict() for item in items])


@inventory_bp.post("/items")
def create_item():
    payload = request.get_json(silent=True) or {}
    valid, err = _validate_payload(payload)
    if not valid:
        return jsonify({"error": err}), 400

    if Item.query.filter_by(sku=payload["sku"]).first():
        return jsonify({"error": "sku already exists"}), 409

    item = Item(
        sku=payload["sku"],
        name=payload["name"],
        quantity=payload["quantity"],
        location=payload.get("location"),
    )
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201


@inventory_bp.put("/items/<int:item_id>")
def update_item(item_id: int):
    item = Item.query.get_or_404(item_id)
    payload = request.get_json(silent=True) or {}

    if "quantity" in payload and (
        not isinstance(payload["quantity"], int) or payload["quantity"] < 0
    ):
        return jsonify({"error": "quantity must be a non-negative integer"}), 400

    for field in ["name", "sku", "quantity", "location"]:
        if field in payload:
            setattr(item, field, payload[field])

    db.session.commit()
    return jsonify(item.to_dict())


@inventory_bp.delete("/items/<int:item_id>")
def delete_item(item_id: int):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return "", 204

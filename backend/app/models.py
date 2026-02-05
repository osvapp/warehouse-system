from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from . import db


role_permissions = db.Table(
    "role_permissions",
    db.Column("role_id", db.Integer, db.ForeignKey("roles.id"), primary_key=True),
    db.Column(
        "permission_id", db.Integer, db.ForeignKey("permissions.id"), primary_key=True
    ),
)


class TimestampMixin:
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class Warehouse(TimestampMixin, db.Model):
    __tablename__ = "warehouses"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(64), nullable=False, unique=True)
    name = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(255), nullable=True)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "location": self.location,
        }


class Item(TimestampMixin, db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(64), nullable=False, unique=True)
    name = db.Column(db.String(120), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    location = db.Column(db.String(120), nullable=True)
    min_stock = db.Column(db.Integer, nullable=False, default=0)
    warehouse_id = db.Column(db.Integer, db.ForeignKey("warehouses.id"), nullable=True)

    warehouse = db.relationship("Warehouse", backref="items")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "sku": self.sku,
            "name": self.name,
            "quantity": self.quantity,
            "location": self.location,
            "min_stock": self.min_stock,
            "warehouse_id": self.warehouse_id,
            "warehouse_name": self.warehouse.name if self.warehouse else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


class WarehouseStaff(TimestampMixin, db.Model):
    __tablename__ = "warehouse_staff"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(32), nullable=True)
    warehouse_id = db.Column(db.Integer, db.ForeignKey("warehouses.id"), nullable=True)

    warehouse = db.relationship("Warehouse", backref="staff")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "warehouse_id": self.warehouse_id,
            "warehouse_name": self.warehouse.name if self.warehouse else None,
        }


class Supplier(TimestampMixin, db.Model):
    __tablename__ = "suppliers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    contact = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(32), nullable=True)

    def to_dict(self) -> dict:
        return {"id": self.id, "name": self.name, "contact": self.contact, "phone": self.phone}


class Customer(TimestampMixin, db.Model):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    contact = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(32), nullable=True)

    def to_dict(self) -> dict:
        return {"id": self.id, "name": self.name, "contact": self.contact, "phone": self.phone}


class InboundOrder(TimestampMixin, db.Model):
    __tablename__ = "inbound_orders"

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey("suppliers.id"), nullable=True)
    quantity = db.Column(db.Integer, nullable=False)
    note = db.Column(db.String(255), nullable=True)

    item = db.relationship("Item")
    supplier = db.relationship("Supplier")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "item_id": self.item_id,
            "item_name": self.item.name if self.item else None,
            "supplier_id": self.supplier_id,
            "supplier_name": self.supplier.name if self.supplier else None,
            "quantity": self.quantity,
            "note": self.note,
            "created_at": self.created_at.isoformat(),
        }


class OutboundOrder(TimestampMixin, db.Model):
    __tablename__ = "outbound_orders"

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=True)
    quantity = db.Column(db.Integer, nullable=False)
    note = db.Column(db.String(255), nullable=True)

    item = db.relationship("Item")
    customer = db.relationship("Customer")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "item_id": self.item_id,
            "item_name": self.item.name if self.item else None,
            "customer_id": self.customer_id,
            "customer_name": self.customer.name if self.customer else None,
            "quantity": self.quantity,
            "note": self.note,
            "created_at": self.created_at.isoformat(),
        }


class InventoryAlert(TimestampMixin, db.Model):
    __tablename__ = "inventory_alerts"

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"), nullable=False)
    current_quantity = db.Column(db.Integer, nullable=False)
    threshold = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(32), nullable=False, default="open")

    item = db.relationship("Item")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "item_id": self.item_id,
            "item_name": self.item.name if self.item else None,
            "current_quantity": self.current_quantity,
            "threshold": self.threshold,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
        }


class Bill(TimestampMixin, db.Model):
    __tablename__ = "bills"

    id = db.Column(db.Integer, primary_key=True)
    bill_no = db.Column(db.String(64), nullable=False, unique=True)
    bill_type = db.Column(db.String(32), nullable=False)
    reference_type = db.Column(db.String(32), nullable=True)
    reference_id = db.Column(db.Integer, nullable=True)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(32), nullable=False, default="draft")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "bill_no": self.bill_no,
            "bill_type": self.bill_type,
            "reference_type": self.reference_type,
            "reference_id": self.reference_id,
            "amount": self.amount,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
        }


class Employee(TimestampMixin, db.Model):
    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    position = db.Column(db.String(120), nullable=True)

    def to_dict(self) -> dict:
        return {"id": self.id, "name": self.name, "email": self.email, "position": self.position}


class Permission(TimestampMixin, db.Model):
    __tablename__ = "permissions"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(64), nullable=False, unique=True)
    name = db.Column(db.String(120), nullable=False)

    def to_dict(self) -> dict:
        return {"id": self.id, "code": self.code, "name": self.name}


class Role(TimestampMixin, db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(64), nullable=False, unique=True)
    name = db.Column(db.String(120), nullable=False)
    permissions = db.relationship("Permission", secondary=role_permissions, backref="roles")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "permissions": [p.to_dict() for p in self.permissions],
        }


class User(TimestampMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=True)

    role = db.relationship("Role")

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "role_id": self.role_id,
            "role_name": self.role.name if self.role else None,
        }

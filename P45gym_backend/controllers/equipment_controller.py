from flask import request

from database.db import db
from models.equipment_model import Equipment
from utils import success_response, error_response, is_number, logger


def _serialize(item):
    return {
        "id": item.id,
        "product_name": item.product_name,
        "category": item.category,
        "price": item.price,
        "stock_quantity": item.stock_quantity,
        "status": item.status,
        "image_url": item.image_url
    }


def _validate(data):
    if not data.get("product_name"):
        return "Product name is required"

    if not data.get("category"):
        return "Category is required"

    if not is_number(data.get("price")) or float(data.get("price")) < 0:
        return "Price must be a non-negative number"

    if not is_number(data.get("stock_quantity", 0)) or float(data.get("stock_quantity", 0)) < 0:
        return "Stock quantity must be a non-negative number"

    return None


# Get all equipment
def get_equipment_list():
    items = Equipment.query.all()
    return [_serialize(i) for i in items]


# Get one equipment item by id
def get_equipment(id):
    item = db.session.get(Equipment, id)
    if not item:
        return error_response("Equipment not found", 404)
    return success_response("Equipment fetched successfully", _serialize(item))


# Add equipment
def add_equipment():
    data = request.get_json(silent=True) or {}

    err = _validate(data)
    if err:
        return error_response(err, 400)

    item = Equipment(
        product_name=data['product_name'],
        category=data['category'],
        price=data['price'],
        stock_quantity=data.get('stock_quantity', 0),
        status=data.get('status', 'In Stock'),
        image_url=data.get('image_url')
    )

    try:
        db.session.add(item)
        db.session.commit()
    except Exception:
        db.session.rollback()
        logger.exception("Failed to add equipment")
        return error_response("Something went wrong, please try again", 500)

    return success_response("Equipment added successfully", _serialize(item), 201)


# Update equipment
def update_equipment(id):
    item = db.session.get(Equipment, id)
    if not item:
        return error_response("Equipment not found", 404)

    data = request.get_json(silent=True) or {}

    err = _validate(data)
    if err:
        return error_response(err, 400)

    item.product_name = data['product_name']
    item.category = data['category']
    item.price = data['price']
    item.stock_quantity = data['stock_quantity']
    item.status = data.get('status', item.status)
    if 'image_url' in data:
        item.image_url = data['image_url']

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        logger.exception("Failed to update equipment %s", id)
        return error_response("Something went wrong, please try again", 500)

    return success_response("Equipment updated successfully", _serialize(item))


# Delete equipment
def delete_equipment(id):
    item = db.session.get(Equipment, id)
    if not item:
        return error_response("Equipment not found", 404)

    try:
        db.session.delete(item)
        db.session.commit()
    except Exception:
        db.session.rollback()
        logger.exception("Failed to delete equipment %s", id)
        return error_response("Something went wrong, please try again", 500)

    return success_response("Equipment deleted successfully")

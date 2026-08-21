from flask import request

from database.db import db
from models.supplement_model import Supplement
from utils import success_response, error_response, is_number, DATE_REGEX, logger


def _serialize(item):
    return {
        "id": item.id,
        "product_name": item.product_name,
        "category": item.category,
        "price": item.price,
        "stock_quantity": item.stock_quantity,
        "expiry_date": item.expiry_date,
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

    expiry = data.get("expiry_date")
    if expiry and not DATE_REGEX.match(expiry):
        return "Expiry date must be in YYYY-MM-DD format"

    return None


# Get all supplements
def get_supplement_list():
    items = Supplement.query.all()
    return [_serialize(i) for i in items]


# Get one supplement by id
def get_supplement(id):
    item = db.session.get(Supplement, id)
    if not item:
        return error_response("Supplement not found", 404)
    return success_response("Supplement fetched successfully", _serialize(item))


# Add supplement
def add_supplement():
    data = request.get_json(silent=True) or {}

    err = _validate(data)
    if err:
        return error_response(err, 400)

    item = Supplement(
        product_name=data['product_name'],
        category=data['category'],
        price=data['price'],
        stock_quantity=data.get('stock_quantity', 0),
        expiry_date=data.get('expiry_date'),
        status=data.get('status', 'In Stock'),
        image_url=data.get('image_url')
    )

    try:
        db.session.add(item)
        db.session.commit()
    except Exception:
        db.session.rollback()
        logger.exception("Failed to add supplement")
        return error_response("Something went wrong, please try again", 500)

    return success_response("Supplement added successfully", _serialize(item), 201)


# Update supplement
def update_supplement(id):
    item = db.session.get(Supplement, id)
    if not item:
        return error_response("Supplement not found", 404)

    data = request.get_json(silent=True) or {}

    err = _validate(data)
    if err:
        return error_response(err, 400)

    item.product_name = data['product_name']
    item.category = data['category']
    item.price = data['price']
    item.stock_quantity = data['stock_quantity']
    item.expiry_date = data.get('expiry_date')
    item.status = data.get('status', item.status)
    if 'image_url' in data:
        item.image_url = data['image_url']

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        logger.exception("Failed to update supplement %s", id)
        return error_response("Something went wrong, please try again", 500)

    return success_response("Supplement updated successfully", _serialize(item))


# Delete supplement
def delete_supplement(id):
    item = db.session.get(Supplement, id)
    if not item:
        return error_response("Supplement not found", 404)

    try:
        db.session.delete(item)
        db.session.commit()
    except Exception:
        db.session.rollback()
        logger.exception("Failed to delete supplement %s", id)
        return error_response("Something went wrong, please try again", 500)

    return success_response("Supplement deleted successfully")

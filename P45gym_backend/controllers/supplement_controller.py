from flask import request, jsonify
from database.db import db
from models.supplement_model import Supplement


# Get all supplements
def get_supplement_list():
    items = Supplement.query.all()
    result = []
    for item in items:
        result.append({
            "id": item.id,
            "product_name": item.product_name,
            "category": item.category,
            "price": item.price,
            "stock_quantity": item.stock_quantity,
            "expiry_date": item.expiry_date,
            "status": item.status
        })
    return jsonify(result)


# Get one supplement by id
def get_supplement(id):
    item = db.session.get(Supplement, id)
    if not item:
        return jsonify({'msg': 'Supplement not found'}), 404

    return jsonify({
        "id": item.id,
        "product_name": item.product_name,
        "category": item.category,
        "price": item.price,
        "stock_quantity": item.stock_quantity,
        "expiry_date": item.expiry_date,
        "status": item.status
    })


# Add supplement
def add_supplement():
    data = request.get_json()
    item = Supplement(
        product_name=data['product_name'],
        category=data['category'],
        price=data['price'],
        stock_quantity=data.get('stock_quantity', 0),
        expiry_date=data.get('expiry_date'),
        status=data.get('status', 'In Stock')
    )
    db.session.add(item)
    db.session.commit()
    return jsonify({'msg': 'Supplement Added Successfully'}), 201


# Update supplement
def update_supplement(id):
    item = db.session.get(Supplement, id)
    if not item:
        return jsonify({'msg': 'Supplement not found'}), 404

    data = request.get_json()
    item.product_name = data['product_name']
    item.category = data['category']
    item.price = data['price']
    item.stock_quantity = data['stock_quantity']
    item.expiry_date = data.get('expiry_date')
    item.status = data['status']

    db.session.commit()
    return jsonify({'msg': 'Supplement Updated Successfully'})


# Delete supplement
def delete_supplement(id):
    item = db.session.get(Supplement, id)
    if not item:
        return jsonify({'msg': 'Supplement not found'}), 404

    db.session.delete(item)
    db.session.commit()
    return jsonify({'msg': 'Supplement Deleted Successfully'})

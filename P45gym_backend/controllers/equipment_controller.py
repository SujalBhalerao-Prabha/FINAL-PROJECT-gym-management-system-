from flask import request, jsonify
from database.db import db
from models.equipment_model import Equipment


# Get all equipment
def get_equipment_list():
    items = Equipment.query.all()
    result = []
    for item in items:
        result.append({
            "id": item.id,
            "product_name": item.product_name,
            "category": item.category,
            "price": item.price,
            "stock_quantity": item.stock_quantity,
            "status": item.status
        })
    return jsonify(result)


# Get one equipment item by id
def get_equipment(id):
    item = db.session.get(Equipment, id)
    if not item:
        return jsonify({'msg': 'Equipment not found'}), 404

    return jsonify({
        "id": item.id,
        "product_name": item.product_name,
        "category": item.category,
        "price": item.price,
        "stock_quantity": item.stock_quantity,
        "status": item.status
    })


# Add equipment
def add_equipment():
    data = request.get_json()
    item = Equipment(
        product_name=data['product_name'],
        category=data['category'],
        price=data['price'],
        stock_quantity=data.get('stock_quantity', 0),
        status=data.get('status', 'In Stock')
    )
    db.session.add(item)
    db.session.commit()
    return jsonify({'msg': 'Equipment Added Successfully'}), 201


# Update equipment
def update_equipment(id):
    item = db.session.get(Equipment, id)
    if not item:
        return jsonify({'msg': 'Equipment not found'}), 404

    data = request.get_json()
    item.product_name = data['product_name']
    item.category = data['category']
    item.price = data['price']
    item.stock_quantity = data['stock_quantity']
    item.status = data['status']

    db.session.commit()
    return jsonify({'msg': 'Equipment Updated Successfully'})


# Delete equipment
def delete_equipment(id):
    item = db.session.get(Equipment, id)
    if not item:
        return jsonify({'msg': 'Equipment not found'}), 404

    db.session.delete(item)
    db.session.commit()
    return jsonify({'msg': 'Equipment Deleted Successfully'})

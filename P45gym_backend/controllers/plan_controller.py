from flask import request, jsonify
from database.db import db
from models.plan_model import Plan


# Get all plans
def get_plans():
    plans = Plan.query.all()
    data = []
    for plan in plans:
        data.append({
            "id": plan.id,
            "plan_name": plan.plan_name,
            "duration_months": plan.duration_months,
            "price": plan.price,
            "status": plan.status
        })
    return jsonify(data)


# Get plan by id
def get_plan(id):
    plan = db.session.get(Plan, id)
    if plan is None:
        return jsonify({'msg': 'Plan not found'}), 404

    return jsonify({
        "id": plan.id,
        "plan_name": plan.plan_name,
        "duration_months": plan.duration_months,
        "price": plan.price,
        "status": plan.status
    })


# Add plan
def add_plan():
    data = request.get_json()
    plan = Plan(
        plan_name=data["plan_name"],
        duration_months=data["duration_months"],
        price=data["price"],
        status=data.get("status", "Active")
    )
    db.session.add(plan)
    db.session.commit()
    return jsonify({"msg": "Plan Added Successfully"}), 201


# Update plan
def update_plan(id):
    plan = db.session.get(Plan, id)

    if plan is None:
        return jsonify({'msg': 'Plan not found'}), 404

    data = request.get_json()

    plan.plan_name = data['plan_name']
    plan.duration_months = data['duration_months']
    plan.price = data['price']
    plan.status = data['status']
    db.session.commit()

    return jsonify({
        'msg': 'Plan Updated Successfully'
    })


# Delete plan
def delete_plan(id):
    plan = db.session.get(Plan, id)

    if plan is None:
        return jsonify({'msg': 'Plan not found'}), 404

    db.session.delete(plan)
    db.session.commit()

    return jsonify({
        'msg': 'Plan Deleted Successfully'
    })

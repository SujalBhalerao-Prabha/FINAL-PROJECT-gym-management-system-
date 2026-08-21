from flask import request

from database.db import db
from models.plan_model import Plan
from utils import success_response, error_response, is_number, logger


def _serialize(plan):
    return {
        "id": plan.id,
        "plan_name": plan.plan_name,
        "duration_months": plan.duration_months,
        "price": plan.price,
        "status": plan.status
    }


def _validate(data):
    if not data.get("plan_name"):
        return "Plan name is required"

    if not is_number(data.get("price")) or float(data.get("price")) <= 0:
        return "Price must be a positive number"

    if not is_number(data.get("duration_months")) or float(data.get("duration_months")) <= 0:
        return "Duration (months) must be a positive number"

    return None


# Get all plans
def get_plans():
    plans = Plan.query.all()
    return [_serialize(p) for p in plans]


# Get plan by id
def get_plan(id):
    plan = db.session.get(Plan, id)
    if plan is None:
        return error_response("Plan not found", 404)
    return success_response("Plan fetched successfully", _serialize(plan))


# Add plan
def add_plan():
    data = request.get_json(silent=True) or {}

    err = _validate(data)
    if err:
        return error_response(err, 400)

    plan = Plan(
        plan_name=data["plan_name"],
        duration_months=data["duration_months"],
        price=data["price"],
        status=data.get("status", "Active")
    )

    try:
        db.session.add(plan)
        db.session.commit()
    except Exception:
        db.session.rollback()
        logger.exception("Failed to add plan")
        return error_response("Something went wrong, please try again", 500)

    return success_response("Plan added successfully", _serialize(plan), 201)


# Update plan
def update_plan(id):
    plan = db.session.get(Plan, id)
    if plan is None:
        return error_response("Plan not found", 404)

    data = request.get_json(silent=True) or {}

    err = _validate(data)
    if err:
        return error_response(err, 400)

    plan.plan_name = data['plan_name']
    plan.duration_months = data['duration_months']
    plan.price = data['price']
    plan.status = data.get('status', plan.status)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        logger.exception("Failed to update plan %s", id)
        return error_response("Something went wrong, please try again", 500)

    return success_response("Plan updated successfully", _serialize(plan))


# Delete plan
def delete_plan(id):
    plan = db.session.get(Plan, id)
    if plan is None:
        return error_response("Plan not found", 404)

    try:
        db.session.delete(plan)
        db.session.commit()
    except Exception:
        db.session.rollback()
        logger.exception("Failed to delete plan %s", id)
        return error_response("Something went wrong, please try again", 500)

    return success_response("Plan deleted successfully")

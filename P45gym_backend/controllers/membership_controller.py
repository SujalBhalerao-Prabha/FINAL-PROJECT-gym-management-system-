from flask import request

from database.db import db
from models.membership_model import Membership
from models.member_model import Member
from models.plan_model import Plan
from utils import success_response, error_response, logger


def _serialize(membership):
    return {
        "id": membership.id,
        "member_id": membership.member_id,
        "member_name": membership.member.name,
        "plan_id": membership.plan_id,
        "plan_name": membership.plan.plan_name,
        "start_date": membership.start_date,
        "end_date": membership.end_date,
        "status": membership.status
    }


# Get all memberships
def get_memberships():
    memberships = Membership.query.all()
    return [_serialize(m) for m in memberships]


# Get membership by id
def get_membership(id):
    membership = db.session.get(Membership, id)
    if not membership:
        return error_response("Membership not found", 404)
    return success_response("Membership fetched successfully", _serialize(membership))


# Add membership
def add_membership():
    data = request.get_json(silent=True) or {}

    if not data.get("start_date") or not data.get("end_date"):
        return error_response("Start date and end date are required", 400)

    member = db.session.get(Member, data.get("member_id"))
    if not member:
        return error_response("Member not found", 404)

    plan = db.session.get(Plan, data.get("plan_id"))
    if not plan:
        return error_response("Plan not found", 404)

    membership = Membership(
        member_id=data["member_id"],
        plan_id=data["plan_id"],
        start_date=data["start_date"],
        end_date=data["end_date"],
        status=data.get("status", "Active")
    )

    try:
        db.session.add(membership)
        db.session.commit()
    except Exception:
        db.session.rollback()
        logger.exception("Failed to add membership")
        return error_response("Something went wrong, please try again", 500)

    return success_response("Membership added successfully", _serialize(membership), 201)


# Update membership
def update_membership(id):
    membership = db.session.get(Membership, id)
    if not membership:
        return error_response("Membership not found", 404)

    data = request.get_json(silent=True) or {}

    if not data.get("start_date") or not data.get("end_date"):
        return error_response("Start date and end date are required", 400)

    membership.start_date = data["start_date"]
    membership.end_date = data["end_date"]
    membership.status = data.get("status", membership.status)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        logger.exception("Failed to update membership %s", id)
        return error_response("Something went wrong, please try again", 500)

    return success_response("Membership updated successfully", _serialize(membership))


# Delete membership
def delete_membership(id):
    membership = db.session.get(Membership, id)
    if not membership:
        return error_response("Membership not found", 404)

    try:
        db.session.delete(membership)
        db.session.commit()
    except Exception:
        db.session.rollback()
        logger.exception("Failed to delete membership %s", id)
        return error_response("Something went wrong, please try again", 500)

    return success_response("Membership deleted successfully")

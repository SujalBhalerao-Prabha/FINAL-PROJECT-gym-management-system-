from flask import request, jsonify
from database.db import db
from models.membership_model import Membership
from models.member_model import Member
from models.plan_model import Plan


# Get all memberships
def get_memberships():
    memberships = Membership.query.all()
    result = []
    for membership in memberships:
        result.append({
            "id": membership.id,
            "member_id": membership.member_id,
            "member_name": membership.member.name,
            "plan_id": membership.plan_id,
            "plan_name": membership.plan.plan_name,
            "start_date": membership.start_date,
            "end_date": membership.end_date,
            "status": membership.status
        })
    return jsonify(result)


# Get membership by id
def get_membership(id):
    membership = db.session.get(Membership, id)

    if not membership:
        return jsonify({"msg": "Membership not found"}), 404

    return jsonify({
        "id": membership.id,
        "member_id": membership.member_id,
        "member_name": membership.member.name,
        "plan_id": membership.plan_id,
        "plan_name": membership.plan.plan_name,
        "start_date": membership.start_date,
        "end_date": membership.end_date,
        "status": membership.status
    })


# Add membership
def add_membership():
    data = request.get_json()
    member = db.session.get(Member, data["member_id"])

    if not member:
        return jsonify({"msg": "Member not found"}), 404

    plan = db.session.get(Plan, data["plan_id"])

    if not plan:
        return jsonify({"msg": "Plan not found"}), 404

    membership = Membership(
        member_id=data["member_id"],
        plan_id=data["plan_id"],
        start_date=data["start_date"],
        end_date=data["end_date"],
        status="Active"
    )
    db.session.add(membership)
    db.session.commit()
    return jsonify({
        "msg": "Membership Added Successfully"
    }), 201


# Update membership
def update_membership(id):
    membership = db.session.get(Membership, id)
    if not membership:
        return jsonify({"msg": "Membership not found"}), 404

    data = request.get_json()
    membership.start_date = data["start_date"]
    membership.end_date = data["end_date"]
    membership.status = data["status"]
    db.session.commit()
    return jsonify({"msg": "Membership Updated Successfully"})


# Delete membership
def delete_membership(id):
    membership = db.session.get(Membership, id)
    if not membership:
        return jsonify({"msg": "Membership not found"}), 404

    db.session.delete(membership)
    db.session.commit()

    return jsonify({
        "msg": "Membership Deleted Successfully"
    })

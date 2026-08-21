from flask import request
from sqlalchemy.exc import IntegrityError

from database.db import db
from models.member_model import Member
from utils import success_response, error_response, EMAIL_REGEX, logger


def _serialize(member):
    return {
        "id": member.id,
        "name": member.name,
        "email": member.email,
        "phone": member.phone,
        "age": member.age
    }


def _validate(data):
    name = data.get("name")
    if not name or not str(name).strip():
        return "Name is required"

    phone = str(data.get("phone", ""))
    if not phone.isdigit():
        return "Phone number must contain only digits"

    email = data.get("email", "")
    if not EMAIL_REGEX.match(email or ""):
        return "Invalid email format"

    return None


# Get all members
def get_members():
    members = Member.query.all()
    return [_serialize(m) for m in members]


# Get member by id
def get_member(id):
    member = db.session.get(Member, id)
    if not member:
        return error_response("Member not found", 404)
    return success_response("Member fetched successfully", _serialize(member))


# Add member
def add_member():
    data = request.get_json(silent=True) or {}

    err = _validate(data)
    if err:
        return error_response(err, 400)

    member = Member(
        name=data['name'],
        email=data['email'],
        phone=str(data['phone']),
        age=data.get('age')
    )

    try:
        db.session.add(member)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return error_response("Email already exists", 400)
    except Exception:
        db.session.rollback()
        logger.exception("Failed to add member")
        return error_response("Something went wrong, please try again", 500)

    return success_response("Member added successfully", _serialize(member), 201)


# Update member
def update_member(id):
    member = db.session.get(Member, id)
    if not member:
        return error_response("Member not found", 404)

    data = request.get_json(silent=True) or {}

    err = _validate(data)
    if err:
        return error_response(err, 400)

    member.name = data['name']
    member.email = data['email']
    member.phone = str(data['phone'])
    member.age = data.get('age')

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return error_response("Email already exists", 400)
    except Exception:
        db.session.rollback()
        logger.exception("Failed to update member %s", id)
        return error_response("Something went wrong, please try again", 500)

    return success_response("Member updated successfully", _serialize(member))


# Delete member
def delete_member(id):
    member = db.session.get(Member, id)
    if not member:
        return error_response("Member not found", 404)

    try:
        db.session.delete(member)
        db.session.commit()
    except Exception:
        db.session.rollback()
        logger.exception("Failed to delete member %s", id)
        return error_response("Something went wrong, please try again", 500)

    return success_response("Member deleted successfully")

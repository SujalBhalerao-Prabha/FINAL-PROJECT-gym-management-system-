from flask import request, jsonify
from database.db import db
from models.member_model import Member


# Get all members
def get_members():
    members = Member.query.all()
    result = []
    for member in members:
        result.append({
            "id": member.id,
            "name": member.name,
            "email": member.email,
            "phone": member.phone,
            "age": member.age
        })
    return jsonify(result)


# Get member by id
def get_member(id):
    member = db.session.get(Member, id)
    if not member:
        return jsonify({'msg': 'Member not found'}), 404

    return jsonify({
        "id": member.id,
        "name": member.name,
        "email": member.email,
        "phone": member.phone,
        "age": member.age
    })


# Add member
def add_member():
    data = request.get_json()
    member = Member(
        name=data['name'],
        email=data['email'],
        phone=data['phone'],
        age=data['age']
    )

    db.session.add(member)
    db.session.commit()
    return jsonify({'msg': 'Member Added Successfully'}), 201


# Update member
def update_member(id):
    member = db.session.get(Member, id)

    if not member:
        return jsonify({'msg': 'Member not found'}), 404

    data = request.get_json()

    member.name = data['name']
    member.email = data['email']
    member.phone = data['phone']
    member.age = data['age']

    db.session.commit()

    return jsonify({'msg': 'Member Updated Successfully'})


# Delete member
def delete_member(id):
    member = db.session.get(Member, id)

    if not member:
        return jsonify({'msg': 'Member not found'}), 404

    db.session.delete(member)
    db.session.commit()
    return jsonify({'msg': 'Member Deleted Successfully'})

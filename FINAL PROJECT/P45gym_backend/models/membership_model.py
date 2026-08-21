from database.db import db


class Membership(db.Model):
    __tablename__ = 'memberships'
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey('plans.id'), nullable=False)
    start_date = db.Column(db.String(20), nullable=False)
    end_date = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(30), nullable=False, default="Active")

    member = db.relationship(
        "Member",
        backref="memberships"
    )

    plan = db.relationship(
        "Plan",
        backref="memberships"
    )

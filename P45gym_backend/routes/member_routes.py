from flask import Blueprint
from controllers.member_controller import (get_members, get_member, add_member, update_member, delete_member)

member_bp = Blueprint("member_bp", __name__)

member_bp.route("/members", methods=["GET"])(get_members)
member_bp.route("/members/<int:id>", methods=["GET"])(get_member)
member_bp.route("/members", methods=["POST"])(add_member)
member_bp.route("/members/<int:id>", methods=["PUT"])(update_member)
member_bp.route("/members/<int:id>", methods=["DELETE"])(delete_member)

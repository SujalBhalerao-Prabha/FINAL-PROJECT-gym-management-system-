from flask import Blueprint
from controllers.membership_controller import (get_memberships, get_membership, add_membership, update_membership, delete_membership)

membership_bp = Blueprint("membership_bp", __name__)

membership_bp.route("/memberships", methods=["GET"])(get_memberships)
membership_bp.route("/memberships/<int:id>", methods=["GET"])(get_membership)
membership_bp.route("/memberships", methods=["POST"])(add_membership)
membership_bp.route("/memberships/<int:id>", methods=["PUT"])(update_membership)
membership_bp.route("/memberships/<int:id>", methods=["DELETE"])(delete_membership)

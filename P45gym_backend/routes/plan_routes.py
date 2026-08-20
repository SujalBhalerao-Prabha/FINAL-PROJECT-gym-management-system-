from flask import Blueprint
from controllers.plan_controller import (get_plans, get_plan, add_plan, update_plan, delete_plan)

plan_bp = Blueprint("plan_bp", __name__)

plan_bp.route("/plans", methods=["GET"])(get_plans)
plan_bp.route("/plans/<int:id>", methods=["GET"])(get_plan)
plan_bp.route("/plans", methods=["POST"])(add_plan)
plan_bp.route("/plans/<int:id>", methods=["PUT"])(update_plan)
plan_bp.route("/plans/<int:id>", methods=["DELETE"])(delete_plan)

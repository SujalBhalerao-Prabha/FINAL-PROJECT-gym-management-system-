from flask import Blueprint
from controllers.equipment_controller import (
    get_equipment_list, get_equipment, add_equipment, update_equipment, delete_equipment
)

equipment_bp = Blueprint("equipment_bp", __name__)

equipment_bp.route("/equipment", methods=["GET"])(get_equipment_list)
equipment_bp.route("/equipment/<int:id>", methods=["GET"])(get_equipment)
equipment_bp.route("/equipment", methods=["POST"])(add_equipment)
equipment_bp.route("/equipment/<int:id>", methods=["PUT"])(update_equipment)
equipment_bp.route("/equipment/<int:id>", methods=["DELETE"])(delete_equipment)

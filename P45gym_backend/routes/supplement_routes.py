from flask import Blueprint
from controllers.supplement_controller import (
    get_supplement_list, get_supplement, add_supplement, update_supplement, delete_supplement
)

supplement_bp = Blueprint("supplement_bp", __name__)

supplement_bp.route("/supplements", methods=["GET"])(get_supplement_list)
supplement_bp.route("/supplements/<int:id>", methods=["GET"])(get_supplement)
supplement_bp.route("/supplements", methods=["POST"])(add_supplement)
supplement_bp.route("/supplements/<int:id>", methods=["PUT"])(update_supplement)
supplement_bp.route("/supplements/<int:id>", methods=["DELETE"])(delete_supplement)

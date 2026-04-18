from flask import Blueprint
from app.gear.controllers.gear_controller import (create_gear, get_all_gear, update_gear, delete_gear)

gear_bp = Blueprint("gear", __name__)

gear_bp.route("/", methods=["GET"])(get_all_gear)
gear_bp.route("/", methods=["POST"])(create_gear)
gear_bp.route("/<int:id>", methods=["PATCH"])(update_gear)
gear_bp.route("/<int:id>", methods=["DELETE"])(delete_gear)
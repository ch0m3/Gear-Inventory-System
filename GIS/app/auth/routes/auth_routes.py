from flask import Blueprint
from app.auth.controllers.auth_controller import register, login, logout
from app.auth.controllers.auth_controller import get_users

auth_bp = Blueprint("auth", __name__)

auth_bp.route("/register", methods = ["POST"])(register)
auth_bp.route("/login", methods = ["POST"])(login)
auth_bp.route("/logout", methods = ["POST"])(logout)
auth_bp.route("/users", methods=["GET"])(get_users)
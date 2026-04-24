from flask import Blueprint, request
from app.auth.models.user_model import create_user, find_user, count_cms
from app.database import get_db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data:
        return {"error": "Invalid JSON"}, 400

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "USER")

    if not all([name, email, password]):
        return {"error": "Missing fields"}, 400

    if role not in ["CM", "USER"]:
        return {"error": "Invalid role"}, 400

    if role == "CM" and count_cms() >= 4:
        return {"error": "Max CM reached"}, 400

    hashed_password = generate_password_hash(password)

    user_id = create_user(name, email, hashed_password, role)

    return {
        "message": "User created",
        "data": {
            "id": user_id,
            "name": name,
            "email": email,
            "role": role
        }
    }, 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data:
        return {"error": "Invalid JSON"}, 400

    email = data.get("email")
    password = data.get("password")

    user = find_user(email)

    if not user or not check_password_hash(user["password"], password):
        return {"error": "Invalid credentials"}, 401

    access_token = create_access_token(
        identity=str(user["id"]),
        additional_claims={"role": user["role"]}
    )

    return {
        "message": "Logged in",
        "access_token": access_token,
        "data": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"]
        }
    }, 200

@auth_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    claims = get_jwt()

    if claims.get("role") != "CM":
        return {"error": "Forbidden"}, 403

    db = get_db()
    users = db.execute(
        "SELECT id, name, email, role FROM users"
    ).fetchall()

    return [dict(user) for user in users], 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_me():
    current_user = get_jwt_identity()

    return {
        "message": "Current user",
        "data": current_user
    }, 200

@auth_bp.route('/logout', methods=['POST'])
def logout():
    # JWT is stateless → logout handled client-side
    return {
        "message": "Logout successful (delete token on client)"
    }, 200
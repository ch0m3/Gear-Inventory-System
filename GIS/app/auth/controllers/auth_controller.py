from flask import request
from app.auth.models.user_model import create_user, find_user, count_cms
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


def register():
    data = request.get_json()

    name = data["name"]
    email = data["email"]
    password = generate_password_hash(data["password"])
    role = data.get("role", "USER")

    # Validate role
    if role not in ["CM", "USER"]:
        return {"error": "Invalid role"}, 400

    # Enforce CM limit
    if role == "CM" and count_cms() >= 4:
        return {"error": "Max CM reached"}, 400

    user_id = create_user(name, email, password, role)

    return {
        "message": "User created",
        "data": {
            "id": user_id,
            "name": name,
            "email": email,
            "role": role
        }
    }, 201


def login():
    data = request.get_json()

    user = find_user(data["email"])

    if not user or not check_password_hash(user["password"], data["password"]):
        return {"error": "Invalid credentials"}, 401

    #JWT token
    token = create_access_token(identity={
        "id": user["id"],
        "role": user["role"]
    })

    return {
        "message": "Logged in",
        "access_token": token,
        "data": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"]
        }
    }, 200


#current logged-in user
@jwt_required()
def get_me():
    user = get_jwt_identity()

    return {
        "message": "Current user",
        "data": user
    }, 200


# Logout is handled client-side 
def logout():
    return {
        "message": "Logout successful (delete token on client)"
    }, 200
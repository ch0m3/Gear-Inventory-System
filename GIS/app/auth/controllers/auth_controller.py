from flask import request, session
from app.auth.models.user_model import create_user, find_user, count_cms
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import get_db
from app.utils.auth_required import login_required, role_required


def register():
    data = request.get_json()

    name = data["name"]
    email = data["email"]
    password = generate_password_hash(data["password"])
    role = data.get("role", "USER")

    if role == "CM" and count_cms()>=4:
        return{"error": "Max CM reached"}, 400
    
    user_id = create_user(name, email, password, role)
    return{"message": "User created",
           "data":{
                "id": user_id,
                "name": name,
                "email": email,
                "role": role
           }}, 201

def login():
    data = request.get_json()
    user = find_user(data["email"])
    if not user or not check_password_hash(user["password"], data["password"]):
        return {"error": "Invalid credentials"}, 401
    
    session["user_id"] = user["id"]
    session["role"] = user["role"]
    return {"message": "Logged in",
            "data": {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"],
                "role": user["role"]
            }
            }, 200


@login_required
@role_required("CM")
def get_users():
    db= get_db()

    users = db.execute("SELECT id, name, email, role FROM users").fetchall()
    return [dict(users) for users in users], 200



def logout():
    session.clear()
    return {"message": "Logged out"}, 200
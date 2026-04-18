from flask import session
from functools import wraps

def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwrgs):
        if "user_id" not in session:
            return{"error": "Unauthorized"},401
        return fn(*args, **kwrgs)
    return wrapper



def role_required(*roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwrgs):
            if "role" not in session:
             return{"error": "Unauthorized"},401
            if session ["role"] not in roles:
             return{"error": "Forbidden"},403
            
            return fn(*args, **kwrgs)
        return wrapper
    return decorator

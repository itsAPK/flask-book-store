from functools import wraps
from flask import abort
from flask_login import current_user
from src.models.user import Role

def role_required(role):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            print(current_user.role)
            if not current_user.role == role:
                abort(403)  # Unauthorized access
            return view_func(*args, **kwargs)
        return wrapper
    return decorator



from functools import wraps
from flask import flash, redirect, session, abort, url_for

def admin_login_required(view_func):
    @wraps(view_func)
    def decorator(*args, **kwargs):
        if not session.get('admin_logged_in'):
             flash('Admin Authentication Required', 'danger')
             return redirect(url_for('admin.login'))
        return view_func(*args, **kwargs)
    return decorator
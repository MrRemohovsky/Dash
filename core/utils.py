from models import db
from functools import wraps
from flask import redirect, url_for, flash
from flask_security import current_user

def bulk_create(list_to_create):
    db.session.add_all(list_to_create)
    db.session.commit()

def login_required(view_func):
    @wraps(view_func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Отказано в доступе!', 'danger')
            return redirect(url_for('session.login'))
        return view_func(*args, **kwargs)
    return decorated_view

def admin_required(view_func):
    @wraps(view_func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Отказано в доступе!', 'danger')
            return redirect(url_for('session.login'))

        user_roles = getattr(current_user, 'roles', [])

        if isinstance(user_roles, list) and any(getattr(role, 'name', '') == 'admin' for role in user_roles):
            return view_func(*args, **kwargs)

        return redirect('/charts')
    return decorated_view
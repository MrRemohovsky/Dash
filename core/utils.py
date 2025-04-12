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
            flash('Вы не авторизованы!', 'danger')
            return redirect(url_for('session.login'))
        return view_func(*args, **kwargs)
    return decorated_view
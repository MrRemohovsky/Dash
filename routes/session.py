from flask import render_template, Blueprint, redirect, request, flash
from flask_security import login_user, current_user, logout_user
from flask_security.utils import verify_password
from core.db_parser import load_data
from core.utils import login_required


session = Blueprint('session', __name__)

@session.route('/')
def index():
    return redirect('/login')

@session.route('/load')
@login_required
def load():
    from app import app

    load_data(app)
    return 'РАБОТА С БД'


@session.route('/login', methods=['GET', 'POST'])
def login():
    from app import user_datastore
    print('1111111111111111')
    if current_user.is_authenticated:
        return redirect('/charts')

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = user_datastore.find_user(email=email)

        if user and verify_password(password, user.password):
            login_user(user)
            return redirect('/charts')
        else:
            flash('Неверный email или пароль.', 'danger')

    return render_template('login.html')

@session.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы успешно вышли из системы.', 'info')
    return redirect('/login')
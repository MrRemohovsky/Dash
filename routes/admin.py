import uuid

from flask import Blueprint, request, render_template, flash, redirect, url_for, jsonify, get_flashed_messages
from flask_security import hash_password
from core.utils import login_required
from models import User, db

admin = Blueprint('admin', __name__)


@admin.route('/admin_panel')
@login_required
def get_all_users():
    page = request.args.get('page', 1, type=int)
    pagination = User.query.paginate(page=page, per_page=10)
    return render_template('admin_panel.html', pagination=pagination)

@admin.route('/admin_panel/create', methods=['POST'])
@login_required
def create_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    patronym = request.form['patronym']
    email = request.form['email']
    password = request.form['password']

    if User.query.filter_by(email=email).first():
        flash('Пользователь с таким email уже существует.', 'warning')
        return jsonify({
            'success': False,
            'messages': get_flashed_messages(with_categories=True)
        })

    if all([first_name, last_name, patronym, email, password]):
        new_user = User(
            id=str(uuid.uuid4())[:4],
            first_name=first_name,
            last_name=last_name,
            patronym=patronym,
            email=email,
            password=hash_password(password),
            active=True,
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Пользователь успешно создан.', 'success')
        return jsonify({
            'success': True,
            'messages': get_flashed_messages(with_categories=True)
        })

    flash('Заполните все поля.', 'danger')
    return jsonify({
        'success': False,
        'messages': get_flashed_messages(with_categories=True)
    })

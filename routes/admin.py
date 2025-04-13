import uuid
from flask import Blueprint, request, render_template, flash, jsonify, get_flashed_messages
from flask_security import hash_password, current_user
from core.utils import admin_required
from models import User, db, Role

admin = Blueprint('admin', __name__)


@admin.route('/admin_panel')
@admin_required
def get_all_users():
    page = request.args.get('page', 1, type=int)
    pagination = User.query.filter_by(active=True).paginate(page=page, per_page=10)
    return render_template('admin_panel.html', pagination=pagination)

@admin.route('/admin_panel/create', methods=['POST'])
@admin_required
def create_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    patronym = request.form['patronym']
    email = request.form['email']
    password = request.form['password']
    role_ids = request.form.getlist('roles')

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
        if role_ids:
            roles = Role.query.filter(Role.id.in_(role_ids)).all()
            new_user.roles = roles
        else:
            new_user.roles = []

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


@admin.route('/admin_panel/deactivate/<string:user_id>', methods=['POST'])
@admin_required
def deactivate_user(user_id):
    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify(success=False, message='Пользователь не найден.')

    if any(role.name.lower() == 'admin' for role in user.roles):
        return jsonify(success=False, message='Нельзя деактивировать администратора.')

    user.active = False
    db.session.commit()
    return jsonify(success=True)

@admin.route('/admin_panel/edit', methods=['POST'])
@admin_required
def edit_user():
    user_id = request.form.get('user_id')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    patronym = request.form.get('patronym')
    email = request.form.get('email')
    password = request.form.get('password')
    role_ids = request.form.getlist('roles')

    if not all([user_id, first_name, last_name, patronym, email]):
        flash('Заполните все поля.', 'warning')
        return jsonify({'success': False, 'messages': get_flashed_messages(with_categories=True)})

    user = User.query.filter_by(id=user_id).first()
    if not user:
        flash('Пользователь не найден.', 'danger')
        return jsonify({'success': False, 'messages': get_flashed_messages(with_categories=True)})

    if User.query.filter(User.email == email, User.id != user_id).first():
        flash('Пользователь с таким email уже существует.', 'danger')
        return jsonify({'success': False, 'messages': get_flashed_messages(with_categories=True)})

    if user != current_user and any(role.name == 'admin' for role in user.roles):
        flash('Вы не можете редактировать данного пользователя!', 'danger')
        return jsonify({'success': False, 'messages': get_flashed_messages(with_categories=True)})

    if role_ids:
        roles = Role.query.filter(Role.id.in_(role_ids)).all()
        user.roles = roles
    else:
        user.roles = []

    user.first_name = first_name
    user.last_name = last_name
    user.patronym = patronym
    user.email = email
    user.password = hash_password(password)
    db.session.commit()

    flash('Данные пользователя обновлены.', 'success')
    return jsonify({'success': True, 'messages': get_flashed_messages(with_categories=True)})

@admin.route('/admin/get_user/<string:user_id>')
@admin_required
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user:
        return jsonify({
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "patronym": user.patronym,
            "email": user.email,
            'roles': [{'id': role.id, 'name': role.name, 'description': role.description} for role in user.roles]
        })

@admin.route('/get_roles')
@admin_required
def get_roles():
    roles = Role.query.all()
    return jsonify([{'id': r.id, 'name': r.name} for r in roles])
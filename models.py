import uuid
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin

db = SQLAlchemy()

class Factory(db.Model):
    __tablename__ = "factory"
    id = db.Column(db.String(4), primary_key=True)
    title = db.Column(db.String(255), unique=True, nullable=False)

    def __repr__(self):
        return f"<Factory {self.title}>"

class Equipment(db.Model):
    __tablename__ = "equipment"
    id = db.Column(db.String(4), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    position = db.Column(db.String(255), nullable=False)
    factory_id = db.Column(db.String(4), db.ForeignKey("factory.id"), nullable=False)
    factory = db.relationship("Factory", backref="equipments")

    def __repr__(self):
        return f"<Equipment {self.title}>"

class Chart(db.Model):
    __tablename__ = "chart"
    id = db.Column(db.String(4), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    time_series = db.Column(db.JSON, nullable=False)
    sensor_type = db.Column(db.String(255), nullable=False)
    unit = db.Column(db.String(10), nullable=False)
    equipment_id = db.Column(db.String(4), db.ForeignKey("equipment.id"), nullable=False)
    equipment = db.relationship("Equipment", backref="charts")

    def __repr__(self):
        return f"<Chart {self.title}>"

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.String(4), db.ForeignKey('user.id')),
    db.Column('role_id', db.String(4), db.ForeignKey('role.id'))
)

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.String(4), primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    patronym = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean())
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    roles = db.relationship('Role', secondary=roles_users,
                           backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return f"<User {self.email}>"

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.String(4), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return f"<Role {self.name}>"
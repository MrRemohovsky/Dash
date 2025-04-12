import os

class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost:5432/dash_db"
    MONITORING_SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost:5432/monitoring_data"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24).hex()
    SECURITY_PASSWORD_SALT = 'f7a9b3e2d8c541f0b6e9d2c8a7f3e5b9'
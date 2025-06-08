import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('MAIN_DATABASE_URL', "postgresql://postgres:postgres@localhost:5432/dash_db")
    MONITORING_SQLALCHEMY_DATABASE_URI = os.getenv('MONITORING_DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/monitoring_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'f1a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r0s1t2u3v4w5x6y7z8')
    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT', 'f7a9b3e2d8c541f0b6e9d2c8a7f3e5b9')
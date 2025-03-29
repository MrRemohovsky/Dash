class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost:5432/dash_db"
    MONITORING_SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost:5432/monitoring_data"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

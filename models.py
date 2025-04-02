from flask_sqlalchemy import SQLAlchemy

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
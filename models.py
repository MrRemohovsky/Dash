from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Factory(db.Model):
    __tablename__ = "factory"
    id = db.Column(db.String(4), primary_key=True)
    title = db.Column(db.String(255), unique=True, nullable=False)

    def __repr__(self):
        return f"<Factory {self.title}>"

class Device(db.Model):
    __tablename__ = "device"
    id = db.Column(db.String(4), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    factory_id = db.Column(db.String(4), db.ForeignKey("factory.id"), nullable=False)
    factory = db.relationship("Factory", backref="devices")

    def __repr__(self):
        return f"<Device {self.title}>"

class Chart(db.Model):
    __tablename__ = "chart"
    id = db.Column(db.String(4), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    time_series = db.Column(db.JSON, nullable=False)
    device_id = db.Column(db.String(4), db.ForeignKey("device.id"), nullable=False)
    device = db.relationship("Device", backref="charts")

    def __repr__(self):
        return f"<Chart {self.title}>"
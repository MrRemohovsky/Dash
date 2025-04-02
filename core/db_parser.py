from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from models import db, Factory, Equipment, Chart
from core.config import Config
from core.utils import bulk_create


MonitoringBase = None


def init_db(app):
    app.config["SQLALCHEMY_BINDS"] = {
        "monitoring": Config.MONITORING_SQLALCHEMY_DATABASE_URI
    }
    db.init_app(app)


def sync_data(app):
    global MonitoringBase
    with app.app_context():
        if MonitoringBase is None:
            engine = db.get_engine(app, bind="monitoring")
            MonitoringBase = automap_base()
            MonitoringBase.prepare(engine, schema="public")
            globals().update(MonitoringBase.classes)

        monitoring_engine = db.get_engine(app, bind="monitoring")
        with Session(bind=monitoring_engine) as monitoring_session:
            SensorData = MonitoringBase.classes.sensor_data
            Sensors = MonitoringBase.classes.sensors
            Workshops = MonitoringBase.classes.workshops
            Equipments = MonitoringBase.classes.equipments

            #Работа с заводами-----------------------------------------------------------
            workshops = monitoring_session.query(Workshops).all()
            new_factories = []
            for workshop in workshops:
                if not Factory.query.filter_by(id=workshop.workshop_id,title=workshop.workshop_name).first():
                    new_factories.append(Factory(id=workshop.workshop_id,title=workshop.workshop_name))
            if new_factories:
                bulk_create(new_factories)

            #Работа с устройствами-------------------------------------------------------
            equipments = monitoring_session.query(Equipments).all()
            new_equipments = []
            for equipment in equipments:
                if not Equipment.query.filter_by(id=equipment.equipment_id, factory_id=equipment.workshop_id).first():
                    new_equipments.append(Equipment(id=equipment.equipment_id, title=equipment.equipment_name,
                                                    factory_id=equipment.workshop_id, position=equipment.equipment_position,))
            if new_equipments:
                bulk_create(new_equipments)

            #Работа с графиками-------------------------------------------------------
            sensors = monitoring_session.query(Sensors).all()
            new_charts = []
            for sensor in sensors:
                sensor_data = monitoring_session.query(SensorData).filter(SensorData.sensor_id == sensor.sensor_id).order_by('timestamp').all()
                time_series = [
                    {"timestamp": str(data.timestamp), "value": data.value}
                    for data in sensor_data
                ]

                if not Chart.query.filter_by(id=sensor.sensor_id, equipment_id=sensor.equipment_id).first():
                    new_charts.append(
                        Chart(id=sensor.sensor_id, title=sensor.variables.variable_name,
                              time_series=time_series, equipment_id=sensor.equipment_id,
                              sensor_type=sensor.type, unit=sensor.unit)
                    )
            if new_charts:
                bulk_create(new_charts)
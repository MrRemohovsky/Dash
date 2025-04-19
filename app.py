import os
from dash import Dash
from flask import Flask
from flask_migrate import Migrate
from routes.admin import admin
from routes.session import session
from routes.dashboard import init_dashboard, dashboard
from core.config import Config
from core.db_parser import init_db, db
from flask_security import Security, SQLAlchemyUserDatastore
from models import User, Role

app = Flask(__name__, static_folder=os.path.join(os.getcwd(), 'templates'))
app.config.from_object(Config)
init_db(app)

migrate = Migrate(app, db)

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore, register_blueprint=False)

dash_app = Dash(__name__, server=app, url_base_pathname='/dashboard/', external_stylesheets=[
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css",
    "/templates/css/dash_styles.css",
])

init_dashboard(dash_app)
app.register_blueprint(session)
app.register_blueprint(dashboard)
app.register_blueprint(admin)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
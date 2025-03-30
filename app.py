import os
from dash import Dash
from flask import Flask, render_template
from flask_migrate import Migrate
from routes.dashboard import init_dashboard
from core.config import Config
from core.db_parser import init_db, db, sync_data

app = Flask(__name__, static_folder=os.path.join(os.getcwd(), 'templates'))
app.config.from_object(Config)
init_db(app)

migrate = Migrate(app, db)

dash_app = Dash(__name__, server=app, url_base_pathname='/dashboard/', external_stylesheets=[
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
])

init_dashboard(dash_app)
@app.route('/')
def index():
    return render_template('base.html')

@app.route('/s')
def s():
    sync_data(app)
    return 'РАБОТА С БД'

if __name__ == "__main__":
    app.run(debug=True)
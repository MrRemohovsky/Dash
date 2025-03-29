from flask import Flask
from flask_migrate import Migrate
from core.config import Config
from core.db_parser import init_db, db, sync_data

app = Flask(__name__)
app.config.from_object(Config)

init_db(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return f"hello world"

@app.route('/s')
def s():
    sync_data(app)
    return 'РАБОТА С БД'

if __name__ == "__main__":
    app.run(debug=True)
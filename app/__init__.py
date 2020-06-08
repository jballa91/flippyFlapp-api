from app.models import db
from flask import Flask
from flask_migrate import Migrate
from .routes import airports, flight_plans
import os

app = Flask(__name__)

app.config.from_mapping({
    'SQLALCHEMY_DATABASE_URI': os.environ.get('DATABASE_URL'),
    'SQLALCHEMY_TRACK_MODIFCATIONS': False,
})

app.register_blueprint(airports.bp)
app.register_blueprint(flight_plans.bp)

db.init_app(app)
Migrate(app, db)

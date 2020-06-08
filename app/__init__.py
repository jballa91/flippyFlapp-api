from app.models import db
from flask import Flask
from flask_migrate import Migrate
from .routes import airports
import os

app = Flask(__name__)

app.config.from_mapping({
    'SQLALCHEMY_DATABASE_URI': os.environ.get('DATABASE_URL'),
    'SQLALCHEMY_TRACK_MODIFCATIONS': False,
})

app.register_blueprint(airports.bp)
db.init_app(app)
Migrate(app, db)

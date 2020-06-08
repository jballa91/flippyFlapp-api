# Flask imports
from app.models import db
from flask import Flask
from flask_migrate import Migrate
from .routes import airports
import os

# Auth0 imports
from .auth import AuthError

# Routes imports
from .routes import airplanes
app = Flask(__name__)

app.register_blueprint(airplanes.bp)


@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


# Don't need required scopes.

app.config.from_mapping({
    'SQLALCHEMY_DATABASE_URI': os.environ.get('DATABASE_URL'),
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
})

app.register_blueprint(airports.bp)
db.init_app(app)
Migrate(app, db)

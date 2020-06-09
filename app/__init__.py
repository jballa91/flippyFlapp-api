# Flask imports
from flask import Flask, request, jsonify, _request_ctx_stack
from flask_migrate import Migrate
from .routes import airports, flight_plans, users, airplanes
from flask_cors import cross_origin, CORS
from .auth import *
from functools import wraps
from six.moves.urllib.request import urlopen
from jose import jwt
from .models import db
import os

# Auth0 imports
from .auth import *


app = Flask(__name__)
app.config.from_mapping({
    'SQLALCHEMY_DATABASE_URI': os.environ.get('DATABASE_URL'),
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
})
cors = CORS(app, resources={r"/*": {"origins": "*"}})

app.register_blueprint(users.bp)
app.register_blueprint(airplanes.bp)


@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


@app.route("/api/public")
@cross_origin(headers=["Content-Type", "Authorization"])
def public():
    response = "Hello from a public endpoint! You don't need to be authenticated to see this."
    return jsonify(message=response)


@app.route("/api/private")
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def private():
    response = "Hello from a private endpoint! You need to be authenticated to see this."
    return jsonify(message=response)

# This needs authorization


@app.route("/api/private-scoped")
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def private_scoped():
    if requires_scope("read:messages"):
        response = "Hello from a private endpoint! You need to be authenticated and have a scope of read:messages to see this."
        return jsonify(message=response)
    raise AuthError({
        "code": "Unauthorized",
        "description": "You don't have access to this resource"
    }, 403)


# Don't need required scopes.
db.init_app(app)
Migrate(app, db)

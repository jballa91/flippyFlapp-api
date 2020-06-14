from flask import Blueprint, jsonify
from flask_cors import cross_origin
from ..auth import *
from ..models import db, User, Airplane, FlightPlan

bp = Blueprint("users", __name__, url_prefix="/users")


@bp.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


@bp.route("/<int:user_id>")
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def get_user():
    body = request.json
    user = User.query.filter_by(email=body["email"]).first()
    return jsonify({"userId": user.id,
                    "email": user.email,
                    "nickname": user.nickname,
                    "name": user.name})


@bp.route("", methods=["PATCH"])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def patch_post_user():
    body = request.json
    print(body)
    user_db = User.query.filter_by(email=body["email"]).first()
    if user_db:
        user_db.nickname = body["nickname"]
        user_db.name = body["name"]
        return jsonify(user_db.toDict())
    else:
        new_user = User(email=body["email"],
                        nickname=body["nickname"],
                        name=body["name"])
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.toDict())


@bp.route('/<int:user_id>/airplanes')
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def getAirPlanes(user_id):
    airplanes = Airplane.query.filter_by(user_id=user_id).all()
    return jsonify([airplane.toDict() for airplane in airplanes])


@bp.route('/<int:user_id>/flightplans')
def getUsersFlightPlans(user_id):
    existingFlightPlans = FlightPlan.query.filter(FlightPlan.user_id == user_id).all()

    return {'data': [plan.toDict() for plan in existingFlightPlans]}

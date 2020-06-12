from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
import json
from ..auth import requires_auth
from ..models import db, Airplane

bp = Blueprint("airplanes", __name__, url_prefix="/airplanes")


@bp.route("/<int:plane_id>")
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def get_airplane(plane_id):
    plane = Airplane.query.get(plane_id)
    print(plane)
    return jsonify(plane.toDict(), 201)
    # return {"data": plane}


@bp.route("", methods=["POST"])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def post_airplane():
    info = request.json
    new_plane = Airplane(name=info['name'],
                         fuel_load=info['fuel_load'],
                         fuel_consumption=info['fuel_consumption'],
                         speed=info['speed'],
                         start_taxi_takeoff_fuel_use=info['start_taxi_takeoff_fuel_use'],
                         user_id=info['user_id'])
    # new_plane = Airplane(**info)
    db.session.add(new_plane)
    db.session.commit()
    return jsonify(new_plane.toDict(), 201)


@ bp.route('/<int:id>')
def getAirPlane(id):
    airplane = Airplane.query.get(id)
    return {'airplane': airplane}

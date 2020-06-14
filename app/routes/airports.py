from flask import Blueprint, request
from ..models import Airport
from flask_cors import cross_origin
import os
import json

bp = Blueprint("airports", __name__, url_prefix='/airports')


@bp.route('/coords')
def getCoords():
    coords = Airport.query.all()
    data = [{'lat': coord.lat, 'lng': coord.lng,
             'id': coord.id} for coord in coords]

    return {"data": data}


@bp.route('/<int:id>')
def getAirport(id):
    airport = Airport.query.get(id)

    data = airport.toDict()
    return {"data": data}


@bp.route('/', methods=['POST'])
@cross_origin(headers=["Content-Type"])
def getAirportByCoord():
    data = request.json

    airport = Airport.query.filter(
        Airport.lat == data['lat'], Airport.lng == data['lng']).one()

    newData = airport.toDict()
    return {"data": newData}

from flask import Blueprint
from ..models import Airport
import os

bp = Blueprint("airports", __name__, url_prefix='/airports')


@bp.route('/coords')
def getCoords():
    coords = Airport.query.all()
    data = [{'lat': coord.lat, 'lng': coord.lon,
             'id': coord.id} for coord in coords]

    return {"data": data}


@bp.route('/<int:id>')
def getAirport(id):
    airport = Airport.query.get(id)

    data = airport.toDict()
    return {"data":data}

@bp.route('/secret')
def getKey():
    key = os.environ.get('GOOGLE_MAP_KEY')

    return {'key':key}

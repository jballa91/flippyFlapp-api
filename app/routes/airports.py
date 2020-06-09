from flask import Blueprint
from ..models import Airport

bp = Blueprint("airports", __name__, url_prefix='/airports')

@bp.route('/coords')
def getCoords():
    coords = Airport.query.all()
    data = [{'x_coord':coord.x_coord, 'y_coord':coord.y_coord, 'id':coord.id} for coord in coords]

    return {"data":data}

@bp.route('/<int:id>')
def getAirport(id):
    airport = Airport.query.get(id)

    data = airport.toDict()
    return {"data":data}

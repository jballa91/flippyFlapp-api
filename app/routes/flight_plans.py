from ..models import FlightPlan, db
from flask import Blueprint, request
from datetime import datetime

bp = Blueprint("flightPlans", __name__, url_prefix='/flightplans')

# make sure dates dont overlap
@bp.route('/', methods=['POST'])
def postFlightPlan():
    data = request.json
    print({**data})
    # start_year = data.startYear
    # start_month = data.startMonth
    # start_day = data.startDay
    # start_hour
    # start_minute
    # start_second
    # end_year
    # end_month
    # end_day
    # end_hour
    # end_minute
    # end_second

    start_date = datetime(data['startYear'], data['startMonth'], data['startDay'], data['startHour'], data['startMinute'], data['startSecond'])
    end_date = datetime(data['endYear'], data['endMonth'], data['endDay'], data['endHour'], data['endMinute'], data['endSecond'])
    print(start_date)
    print(end_date)
    flightPlan = FlightPlan(start_date=start_date, end_date=end_date, name=data['name'], route=data['route'], user_id=data['user_id'])
    db.session.add(flightPlan)
    db.session.commit()

    return 'got through'

@bp.route('/<int:id>', methods=['PATCH'])
def patchFlightPlan():
    pass

@bp.route('/<int:id>')
def getFlightPlan():
    flightPlan = FlightPlan.query.options(joinedload(FlightPlan.user)).get(id)
    data = flightPlan.toDict()
    return {'data': data}

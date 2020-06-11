from ..models import FlightPlan, db
from flask import Blueprint, request
from datetime import datetime
from sqlalchemy.orm import joinedload
from ..routes import routes_bearing, routes_cond

bp = Blueprint("flightPlans", __name__, url_prefix='/flightplans')

# checks to make sure date intervals dont overlap


def isOverlap(start1, end1, start2,
              end2): return end1 >= start2 and end2 >= start1


@bp.route('/', methods=['POST'])
def postFlightPlan():
    data = request.json

    # get a users flight plans
    userId = 1
    existingFlightPlans = FlightPlan.query.filter(
        FlightPlan.user_id == userId).all()

    # get dates from request object and map to datetime obj
    start_date_to_enter = datetime(data['startYear'], data['startMonth'],
                                   data['startDay'], data['startHour'], data['startMinute'], data['startSecond'])
    end_date_to_enter = datetime(data['endYear'], data['endMonth'],
                                 data['endDay'], data['endHour'], data['endMinute'], data['endSecond'])

    # makes sure dates dont overlap with existing date
    for date in existingFlightPlans:
        start = date.start_date
        end = date.end_date
        if (isOverlap(start_date_to_enter, end_date_to_enter, start, end)):
            return f'Date entered overlaps with flight plan {date.name}'
        # special case if dates match exactly
        elif (start_date_to_enter == start or end_date_to_enter == end):
            return f'Date entered matches {date.name}'
        elif(start_date_to_enter >= end_date_to_enter):
            return 'end date is before the start date'

    flightPlan = FlightPlan(start_date=start_date_to_enter, end_date=end_date_to_enter,
                            name=data['name'], route=data['route'], user_id=data['user_id'])
    db.session.add(flightPlan)
    db.session.commit()

    return 'got through'


@bp.route('/pathcalc', methods=['POST'])
def postPathCalc():
    {departure, destination, range, opt} = request.json
    opt_cond = routes_cond(departure, destination, range, opt)
    opt_bearing = routes_bearing(departure, destination, range, opt)
    if opt_bearing and opt_cond and opt:
        opts = [opt_bearing, opt_cond]
        opt = sorted(opts, key=lambda k: k['distance'])[0]
    elif opt_bearing and opt_cond:
        opts = [opt_bearing, opt_cond]
        opt = sorted(opts, key=lambda k: k['landings'])[0]
    elif opt_bearing:
        opt = opt_bearing
    else:
        opt = opt_cond
    return {'route': opt}
# to-do--------------------------------------------------------------


@bp.route('/<int:id>', methods=['PATCH'])
def patchFlightPlan(id):
    pass


@bp.route('/<int:id>')
def getFlightPlan(id):
    flightPlan = FlightPlan.query.options(joinedload(FlightPlan.user)).get(id)
    data = flightPlan.toDictJoinedLoad()
    return {'data': data}

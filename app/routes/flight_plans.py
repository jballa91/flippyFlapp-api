from ..models import FlightPlan, Airport, db
from flask import Blueprint, request
from datetime import datetime
from sqlalchemy.orm import joinedload
from ..auth import requires_auth
from flask_cors import cross_origin

from ..routescalc import routes_cond
from ..routescalc import routes_bearing

from ..range import find_range
import json


bp = Blueprint("flightPlans", __name__, url_prefix='/flightplans')

# checks to make sure date intervals dont overlap


def isOverlap(start1, end1, start2,
              end2): return end1 >= start2 and end2 >= start1


@bp.route('/', methods=['POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def postFlightPlan():
    errors = []
    data = request.json
    print(data['route'])
    # get a users flight plans
    userId = data['user_id']
    print(data['name'])
    existingFlightPlans = FlightPlan.query.filter(
        FlightPlan.user_id == userId).all()

    # get dates from request object and map to datetime obj
    start_date_to_enter = datetime(data['startYear'], data['startMonth'],
                                   data['startDay'], data['startHour'], data['startMinute'], 0)
    end_date_to_enter = datetime(data['endYear'], data['endMonth'],
                                 data['endDay'], data['endHour'], data['endMinute'], 0)

    # makes sure dates dont overlap with existing date
    for date in existingFlightPlans:
        start = date.start_date
        end = date.end_date
        if (isOverlap(start_date_to_enter, end_date_to_enter, start, end)):
            errors.append(f'Date entered overlaps with flight plan {date.name}')
        # special case if dates match exactly
        elif (start_date_to_enter == start or end_date_to_enter == end):
            errors.append(f'Date entered matches "{date.name}"')
    if(start_date_to_enter >= end_date_to_enter):
        errors.append('end date is before or equal to the start date')
    if(data['name'] == ''):
        errors.append('Please enter a name ')

    if(len(errors) == 0):
        flightPlan = FlightPlan(start_date=start_date_to_enter, end_date=end_date_to_enter,
                                name=data['name'], route=data['route'], user_id=data['user_id'])
        db.session.add(flightPlan)
        db.session.commit()
        return {'data': 'It Worked'}
    else:
        return {'errors': errors}




@bp.route('/pathcalc', methods=['POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def postPathCalc():
    data = request.json
    # print(data)
    departure = {"lat": data['startPoint']
                 ["lat"], "lng": data['startPoint']['lon']}

    destination = {"lat": data['endPoint']
                   ["lat"], "lng": data['endPoint']['lon']}
    fuel_load = data['airplane']['fuel_load']
    start_taxi_takeoff_fuel_use = data['airplane']['start_taxi_takeoff_fuel_use']
    fuel_consumption = data['airplane']['fuel_consumption']
    speed = data['airplane']['speed']
    opt = data['opt']
    airports = Airport.query.all()
    lat2 = Airport.query.with_entities(Airport.lat)
    lng2 = Airport.query.with_entities(Airport.lng)
    airports = [{'lat': x, 'lng': y} for (x,), (y,) in zip(lat2, lng2)]
    airplane_range = find_range(fuel_load, start_taxi_takeoff_fuel_use,
                                fuel_consumption, speed)

    opt_cond = routes_cond(departure, destination,
                           airplane_range, opt, airports)
    opt_bearing = routes_bearing(
        departure, destination, airplane_range, opt, airports)

    if opt_bearing and opt_cond and opt:
        optroutes = [opt_bearing, opt_cond]
        optroute = sorted(optroutes, key=lambda k: k['distance'])[0]
    elif opt_bearing and opt_cond:
        optroutes = [opt_bearing, opt_cond]
        optroute = sorted(optroutes, key=lambda k: k['landings'])[0]
    elif opt_bearing:
        optroute = opt_bearing
    else:
        optroute = opt_cond
    optroute_list = []
    print('this')
    print(optroute_list)
    # print(len(optroute))
    print(optroute)
    print(range(1, int(len(optroute))))
    for stop in range(1, (len(optroute)-1)):
        print("stops", str(stop))
        optroute_list.append(optroute[str(stop)])
    print("list", optroute_list)
    return {'route': optroute_list}

# to-do--------------------------------------------------------------


@ bp.route('/<int:id>', methods=['PATCH'])
def patchFlightPlan(id):
    pass


@ bp.route('/<int:id>')
def getFlightPlan(id):
    flightPlan = FlightPlan.query.options(joinedload(FlightPlan.user)).get(id)
    data = flightPlan.toDictJoinedLoad()
    return {'data': data}

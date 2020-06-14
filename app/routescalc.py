# from geo import find_distance_and_bearing, find_next_reference
from .distance import distance
from .bearing import bearing_calc, next_reference
from .models import Airport, db
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker
import os
import copy

conversion = 0.539957 / 1000
# db_url = os.environ.get('DATABASE_URL')
# engine = create_engine(db_url)

# SessionFactory = sessionmaker(bind=engine)

# session = SessionFactory()
# lat = session.query(Airport.lat)
# lng = session.query(Airport.lng)
# airports = [{'lat': x, 'lng': y} for (x,), (y,) in zip(lat, lng)]


def routes_cond(departure, destination, range, opt, airports):
    final_paths = []
    flight_distance = distance(departure, destination)
    if flight_distance / range > 2:
        return []
    if flight_distance <= range:
        final_paths = [{"distance": flight_distance,
                        "landings": 1, "1": departure, "2": destination}]
        return final_paths[0]

    paths = [{"distance": 0, "landings": 0, "1": departure}]
    counter = 0
    while len(paths) and counter < 1000:
        counter += 1

        path = paths.pop(0)
        departure = path[str(len(path)-2)]

        if distance(departure, destination) > range:

            possible_airports = [j for j in airports if range*0.85 <= distance(departure, j) <= range and distance(departure, j) <= distance(
                departure, destination) and distance(destination, j) <= distance(departure, destination)]

            # possible_airports = [j for j in airports if
            #                      range *
            #                      0.8 <= find_distance_and_bearing(
            #                          departure, j)['s12'] * conversion <= range
            #                      and find_distance_and_bearing(departure, j)['s12'] * conversion <= find_distance_and_bearing(departure, destination)['s12'] * conversion
            #                      and find_distance_and_bearing(destination, j)['s12'] * conversion <= find_distance_and_bearing(departure, destination)['s12'] * conversion]

            for i in possible_airports:

                new_path = copy.deepcopy(path)

                new_path[str(len(new_path)-1)] = i

                new_path["distance"] += distance(departure, i)
                new_path["landings"] += 1

                paths.append(new_path)
        else:

            new_path = copy.deepcopy(path)

            new_path[str(len(new_path)-1)] = destination

            new_path["distance"] += distance(departure, destination)
            new_path["landings"] += 1
            final_paths.append(new_path)

    if len(final_paths) and opt:
        final_paths = sorted(final_paths, key=lambda k: k['distance'])[0]
    elif len(final_paths):
        final_paths = sorted(final_paths, key=lambda k: k['landings'])[0]

    return(final_paths)


def routes_bearing(departure, destination, range, opt, airports):

    final_paths = []
    # flight_distance = find_distance_and_bearing(
    flight_distance = distance(
        # departure, destination)['s12'] * conversion
        departure, destination)

    if flight_distance <= range:
        final_paths = [{"distance": flight_distance,
                        "landings": 1, "1": departure, "2": destination}]
        return final_paths[0]

    paths = [{"distance": 0, "landings": 0, "1": departure}]
    while len(paths):

        path = paths.pop(0)
        departure = path[str(len(path)-2)]

        # if find_distance_and_bearing(departure, destination)['s12'] * conversion > range:
        if distance(departure, destination) > range:

            bearing = bearing_calc(departure, destination)
            reference_point_lat = next_reference(
                departure, bearing, range)['lat2']
            reference_point_lng = next_reference(
                departure, bearing, range)['lng2']
            reference_point = {'lat': reference_point_lat,
                               'lng': reference_point_lng}
            possible_airports = [j for j in airports if distance(
                reference_point, j) <= range * 0.1]

            for i in possible_airports:

                new_path = copy.deepcopy(path)

                new_path[str(len(new_path)-1)] = i

                new_path["distance"] += distance(departure, i)
                new_path["landings"] += 1

                paths.append(new_path)
        else:

            new_path = copy.deepcopy(path)

            new_path[str(len(new_path)-1)] = destination

            new_path["distance"] += distance(departure, destination)
            new_path["landings"] += 1
            final_paths.append(new_path)
    if len(final_paths) and opt:
        final_paths = sorted(final_paths, key=lambda k: k['distance'])[0]
    elif len(final_paths):
        final_paths = sorted(final_paths, key=lambda k: k['landings'])[0]

    return(final_paths)

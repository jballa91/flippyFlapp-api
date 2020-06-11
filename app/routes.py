from geo import find_distance_and_bearing, find_next_reference
from distance import distance
from models import Airport
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker
import os
import copy
conversion = 0.621371 / 1000
db_url = os.environ.get('DATABASE_URL')
engine = create_engine(db_url)

SessionFactory = sessionmaker(bind=engine)

session = SessionFactory()
lat = session.query(Airport.lat)
lon = session.query(Airport.lon)
airports = [{'lat': x, 'lon': y} for (x,), (y,) in zip(lat, lon)]


def routes_cond(departure, destination, range, opt=False):
    final_paths = []
    flight_distance = distance(departure, destination)

    if flight_distance <= range:
        final_paths = [departure, destination]
        return final_paths

    paths = [{"distance": 0, "landings": 0, "1": departure}]
    while len(paths):

        path = paths.pop(0)
        departure = path[str(len(path)-2)]

        if distance(departure, destination) > range:

            possible_airports = [j for j in airports if range*0.75 <= distance(departure, j) <= range and distance(departure, j) <= distance(
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


def routes_bearing(departure, destination, range, opt=False):
    final_paths = []
    flight_distance = find_distance_and_bearing(
        departure, destination)['s12'] * conversion

    if flight_distance <= range:
        final_paths = [departure, destination]
        return final_paths

    paths = [{"distance": 0, "landings": 0, "1": departure}]
    while len(paths):

        path = paths.pop(0)
        departure = path[str(len(path)-2)]

        if find_distance_and_bearing(departure, destination)['s12'] * conversion > range:
            bearing = find_distance_and_bearing(departure, destination)['azi1']
            reference_point_lat = find_next_reference(
                departure, bearing, range*0.8 / conversion)['lat2']
            reference_point_lon = find_next_reference(
                departure, bearing, range*0.8 / conversion)['lon2']
            reference_point = {'lat': reference_point_lat,
                               'lon': reference_point_lon}

            possible_airports = [j for j in airports if find_distance_and_bearing(
                reference_point, j)['s12'] * conversion <= range * 0.1]

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


print(routes_bearing({'lon': -115.32524999993736, 'lat': 33.74772222164236},
                     {'lon': -120.88694444435187, 'lat': 38.4400000002395}, 250))

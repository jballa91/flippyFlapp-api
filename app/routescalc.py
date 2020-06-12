from geo import find_distance_and_bearing, find_next_reference
from distance import distance
from models import Airport
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker
import os
import copy

conversion = 0.539957 / 1000
db_url = os.environ.get('DATABASE_URL')
engine = create_engine(db_url)

SessionFactory = sessionmaker(bind=engine)

session = SessionFactory()
lat = session.query(Airport.lat)
lng = session.query(Airport.lng)
airports = [{'lat': x, 'lng': y} for (x,), (y,) in zip(lat, lng)]


def routes_cond(departure, destination, range, opt=False):
    final_paths = []
    flight_distance = distance(departure, destination)
    if flight_distance / range > 3:
        return []
    if flight_distance <= range:
        final_paths = [{"distance": flight_distance,
                        "landings": 1, "1": departure, "2": destination}]
        return final_paths[0]

    paths = [{"distance": 0, "landings": 0, "1": departure}]
    counter = 0
    while len(paths):
        counter += 1
        print(paths)
        print(counter)

        path = paths.pop(0)
        departure = path[str(len(path)-2)]

        if distance(departure, destination) > range:

            possible_airports = [j for j in airports if range*0.8 <= distance(departure, j) <= range and distance(departure, j) <= distance(
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
        final_paths = [{"distance": flight_distance,
                        "landings": 1, "1": departure, "2": destination}]
        return final_paths[0]

    paths = [{"distance": 0, "landings": 0, "1": departure}]
    while len(paths):

        path = paths.pop(0)
        departure = path[str(len(path)-2)]

        if find_distance_and_bearing(departure, destination)['s12'] * conversion > range:
            bearing = find_distance_and_bearing(departure, destination)['azi1']
            # print(find_next_reference(
            #     departure, bearing, range*0.8 / conversion))
            reference_point_lat = find_next_reference(
                departure, bearing, range*0.8 / conversion)['lat2']
            reference_point_lng = find_next_reference(
                departure, bearing, range*0.8 / conversion)['lon2']
            reference_point = {'lat': reference_point_lat,
                               'lng': reference_point_lng}

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


# print(routes_cond({'lat': 33.74772222164236, 'lng': -115.32524999993736},
#                   #   {'lat': 38.4400000002395, 'lng': -120.88694444435187}, 250))
#                   {'lat': 42.20844291715825, 'lng': -75.97960727836056}, 250))
# #   {'lat': 54.144611110832585, 'lng': -165.604108332967}, 250))

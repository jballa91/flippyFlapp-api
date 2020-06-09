from distance import distance
from models import AirPort
from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import os
import copy

db_url = os.environ.get('DATABASE_URL')
engine = create_engine(db_url)

SessionFactory = sessionmaker(bind=engine)

session = SessionFactory()
x_coord = session.query(AirPort.x_coord)
y_coord = session.query(AirPort.y_coord)
airports = [{'x': x, 'y': y} for (x,), (y,) in zip(x_coord, y_coord)]


def routes(departure, destination, range):
    final_paths = []
    flight_distance = distance(departure, destination)
    if flight_distance <= range:
        final_paths = [departure, destination]
        return final_paths

    paths = [{"distance": 0, "landings": 0, "1": departure}]
    while len(paths):
        path = paths.pop(0)
        departure = path[str(len(path)-2)]

        possible_airports = [j for j in airports if range*0.8 <= distance(departure, j) <= range and distance(departure, j) <= distance(
            departure, destination) and distance(destination, j) <= distance(departure, destination)]

        for i in possible_airports:

            new_path = copy.deepcopy(path)

            new_path[str(len(new_path)-1)] = i

            new_path["distance"] += distance(departure, i)
            new_path["landings"] += 1

            if new_path[str(len(new_path)-2)] == destination:
                final_paths.append(new_path)

            elif new_path["distance"] < 1.5 * flight_distance and new_path["landings"] < flight_distance / range + 1:
                paths.append(new_path)

    return(final_paths)


print(routes({'x': -115.32524999993736, 'y': 33.74772222164236},
             {'x': -120.88694444435187, 'y': 38.4400000002395}, 250))

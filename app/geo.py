
from geographiclib.geodesic import Geodesic


def find_distance_and_bearing(latlon1, latlon2):
    lat1 = latlon1['lat']
    lon1 = latlon1['lon']
    lat2 = latlon2['lat']
    lon2 = latlon2['lon']

    return Geodesic.WGS84.Inverse(lat1, lon1, lat2, lon2)


def find_next_reference(latlon, bearing, range):
    lat = latlon['lat']
    lon = latlon['lon']
    return Geodesic.WGS84.Direct(lat, lon, bearing, range)
# Nautical Miles
# def find_range(airplane):
#     fuel_load = airplane["fuel_load"]
#     start_fuel = airplane["start_fuel"]
#     fuel_rate = airplane["fuel_consumption"]
#     speed = airplane["speed"]

#     usable_fuel = fuel_load - \
#         start_fuel-(fuel_rate/2)
#     fuel_to_endpoint = .9*usable_fuel
#     air_time = fuel_to_endpoint/fuel_rate
#     range = 115*air_time

#     range = find_range(airplane)
#     print(range)
#     bearing = find_bearing(a, b)
#     bearing = math.radians(bearing)
#     print(f"bearing {bearing}")
#     ax = math.radians(a[0])
#     ay = math.radians(a[1])
#     R = 3440.1
#     lil_delta = range/R

#     lat = (math.asin((math.sin(ax)*math.cos(lil_delta)) +
#                      (math.cos(ax)*math.sin(lil_delta)*math.cos(bearing))))
#     lon = (ay + math.atan2(math.sin(bearing)*math.sin(lil_delta)
#                            * math.cos(ax), math.cos(lil_delta)-math.sin(ax)*math.sin(lat)))
#     lat = math.degrees(lat)
#     lon = math.degrees(lon)
#     return (lat, lon)
# # Point on a line following a bearing, for a distance(range)
# def destination_point(airplane, a, b):
#     range = find_range(airplane)
#     print(range)
#     bearing = find_bearing(a, b)
#     bearing = math.radians(bearing)
#     print(f"bearing {bearing}")
#     ax = math.radians(a[0])
#     ay = math.radians(a[1])
#     R = 3440.1
#     lil_delta = range/R

#     lat = (math.asin((math.sin(ax)*math.cos(lil_delta)) +
#                      (math.cos(ax)*math.sin(lil_delta)*math.cos(bearing))))
#     lon = (ay + math.atan2(math.sin(bearing)*math.sin(lil_delta)
#                            * math.cos(ax), math.cos(lil_delta)-math.sin(ax)*math.sin(lat)))
#     lat = math.degrees(lat)
#     lon = math.degrees(lon)
#     return (lat, lon)


# c = (destination_point(airplane, a, b))
# # print(find_distance(a, b))
# # print(find_bearing(a, b))
# # print(find_range(airplane))
# print(destination_point(airplane, a, b))
# print(find_distance(a, c))
# print(find_distance((-115.32524999993736, 33.74772222164236),
#                     (-120.88694444435187, 38.4400000002395)))

# print(find_bearing((-115.32524999993736, 33.74772222164236),
#                    (-120.88694444435187, 38.4400000002395)))

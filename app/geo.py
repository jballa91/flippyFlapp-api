
from geographiclib.geodesic import Geodesic


def find_distance_and_bearing(latlon1, latlon2):
    lat1 = latlon1['lat']
    lng1 = latlon1['lng']
    lat2 = latlon2['lat']
    lng2 = latlon2['lng']

    return Geodesic.WGS84.Inverse(lat1, lng1, lat2, lng2)


def find_next_reference(latlon, bearing, range):
    lat = latlon['lat']
    lng = latlon['lng']
    return Geodesic.WGS84.Direct(lat, lng, bearing, range)

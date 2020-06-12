# Haversine formula:
# a = sin²(Δφ/2) + cos φ1 ⋅ cos φ2 ⋅ sin²(Δλ/2)
# c = 2 ⋅ atan2( √a, √(1−a) )
# d = R ⋅ c
# where	φ is latitude, λ is lnggitude, R is earth’s radius (mean radius = 6,371km);
# note that angles need to be in radians to pass to trig functions!
import math


def distance(coordinates1, coordinates2):

    lat1 = coordinates1["lat"]
    lng1 = coordinates1["lng"]

    lat2 = coordinates2["lat"]
    lng2 = coordinates2["lng"]

    R = 6371e3  # metres
    φ1 = lat1 * math.pi/180  # φ, λ in radians
    φ2 = lat2 * math.pi/180
    Δφ = (lat2-lat1) * math.pi/180
    Δλ = (lng2-lng1) * math.pi/180

    a = math.sin(Δφ/2) * math.sin(Δφ/2) + math.cos(φ1) * \
        math.cos(φ2) * math.sin(Δλ/2) * math.sin(Δλ/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    distance = R * c * 0.539957 / 1000  # in miles
    return distance


# print(distance({'x': 134.54425000033328, 'y': 7.367305556162343},
#                {'x': -108.12205555585666, 'y': 43.25097222169987}))

# print(distance({'x': -115.32524999993736, 'y': 33.74772222164236},
#                {'x': -120.88694444435187, 'y': 38.4400000002395}))

import math


def bearing_calc(latlng1, latlng2):
    lat1 = latlng1['lat']
    lng1 = latlng1['lng']
    lat2 = latlng2['lat']
    lng2 = latlng2['lng']
    # Calculating Bearing or Heading angle between two points:
    # So if you are from GIS field or dealing with GIS application, you should know bearing and how to calculate bearing with formula. Let us look on formula and tool for bearing:

    # Let ‘R’ be the radius of Earth,
    # ‘L’ be the longitude,
    # ‘θ’ be latitude,
    # ‘β‘ be Bearing.
    # Denote point A and B as two different points, where ‘La’ is point A longitude and ‘θa’ is point A latitude, similarly assume for point B. Bearing would be measured from North direction i.e 0° bearing means North, 90° bearing is East, 180° bearing is measured to be South, and 270° to be West.

    # Note: If bearing is denoted with +ve or –ve initials whose values lies between 0° to 180°, then –ve is denoted for South and West sides.

    # Formula to find Bearing, when two different points latitude, longitude is given:
    # Bearing from point A to B, can be calculated as,

    # β = atan2(X, Y),

    # where, X and Y are two quantities and can be calculated as:

    # X = cos θb * sin ∆L

    # Y = cos θa * sin θb – sin θa * cos θb * cos ∆L

    # Lets us take an example to calculate bearing between the two different points with the formula:

    # Kansas City: 39.099912, -94.581213
    # St Louis: 38.627089, -90.200203
    # So X and Y can be calculated as,

    X = math.cos(lat2 * math.pi / 180) * math.sin((lng2-lng1) * math.pi / 180)

    # X = 0.05967668696

    # And
    Y = math.cos(lat1 * math.pi / 180) * math.sin(lat2 * math.pi / 180) - math.sin(lat1 *
                                                                                   math.pi / 180) * math.cos(lat2 * math.pi / 180) * math.cos((lng2-lng1) * math.pi / 180)
    # Y = math.cos(39.099912) * math.sin(38.627089) – math.sin(39.099912) * math.cos(38.627089) * math.cos(4.38101)

    # Y = 0.77604737571 * 0.62424902378 – 0.6306746155 * 0.78122541965 * 0.99707812506

    # Y = -0.00681261948

    # ***Convert θ into radians***
    B = math.atan2(X, Y)
    # = atan2(0.05967668696, -0.00681261948) = 1.684463062558 radians
    # So as, β = math.atan2(X, Y)

    # convert it into degree

    # β = 96.51°

    # This means, from Kansas City if we move in 96.51° bearing direction, we will reach St Louis.
    return (B)


def next_reference(latlon, bearing, range):
    lat = latlon['lat']
    lng = latlon['lng']

    R = 6371e3 * 0.539957 / 1000  # Radius of the Earth
    # brng = 1.57  # Bearing is 90 degrees converted to radians.
    # d = 15  # Distance in km

    # # lat2  52.20444 - the lat result I'm hoping for
    # # lon2  0.36056 - the long result I'm hoping for.

    lat = lat * (math.pi / 180)  # Current lat point converted to radians
    lng = lng * (math.pi / 180)  # Current long point converted to radians

    lat2 = math.asin(math.sin(lat)*math.cos(range/R) +
                     math.cos(lat)*math.sin(range/R)*math.cos(bearing))

    lng2 = lng + math.atan2(math.sin(bearing)*math.sin(range/R)*math.cos(lat),
                            math.cos(range/R)-math.sin(lat)*math.sin(lat2))

    lat2 = lat2 * 180 / math.pi
    lng2 = lng2 * 180 / math.pi

    return ({'lat2': lat2, 'lng2': lng2})

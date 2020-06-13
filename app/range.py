def find_range(fuel_load, start_taxi_takeoff_fuel_use, fuel_consumption, speed):
    # fuel_load = airplane[""]
    # start_fuel = airplane[""]
    # fuel_rate = airplane[""]
    # speed = airplane[""]
    usable_fuel = fuel_load - start_taxi_takeoff_fuel_use
    # start_fuel-(fuel_rate/2)
    fuel_to_endpoint = .9*usable_fuel
    air_time = fuel_to_endpoint/fuel_consumption
    range = speed*air_time
    return range
# Point on a line following a bearing, for a distance(range)
# Find max legal range from the endpoint


def find_range_from_endpoint(airplane):
    fuel_load = airplane["fuel_load"]
    start_fuel = airplane["start_fuel"]
    fuel_rate = airplane["fuel_consumption"]
    speed = airplane["speed"]
    usable_fuel = fuel_load - \
        start_fuel-(fuel_rate/2)
    fuel_from_endpoint = .1*usable_fuel
    air_time = fuel_from_endpoint/fuel_rate
    range = 115*air_time
    return range

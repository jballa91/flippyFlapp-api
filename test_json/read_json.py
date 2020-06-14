import json
f = open("test_json.txt", "r")

jsonData = f.read()


parsed = json.loads(jsonData)

i = 1
airports = []
for airport in parsed["features"]:
    current_airport = {}
    current_airport["id"] = i
    current_airport["y_coord"] = airport['geometry']['x']
    current_airport["x_coord"] = airport['geometry']['y']
    current_airport["name"] = airport['attributes']['Fac_Name']
    current_airport["city"] = airport['attributes']['City']
    current_airport["State"] = airport['attributes']['State_Post_Office_Code']
    current_airport["loc_id"] = airport['attributes']['Loc_Id']
    current_airport["manager_name"] = airport['attributes']['Manager_Name']
    current_airport["manager_phone_number"] = airport['attributes']['Manager_Phone']
    current_airport["fss_phone_number"] = airport['attributes']['Local_Phone_Airport_To_Fss']
    current_airport["sectional_chart"] = airport['attributes']['Sectional_Chart']
    current_airport["elevation"] = airport['attributes']['Elevation']

    current_airport["pattern_altitude"] = airport['attributes']['Pattern_Altitude']

    current_airport["fuel_types"] = airport['attributes']['Fuel_Type']
    current_airport["atc_tower"] = airport['attributes']['Atc_Tower']
    current_airport["ctaf"] = airport['attributes']['Ctaf']
    current_airport["landing_fee"] = airport['attributes']['Landing_Fee']
    airports.append(current_airport)
    i += 1

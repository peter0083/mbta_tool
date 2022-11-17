from pprint import pprint

import requests
from typing import List, Dict, Tuple

# method 1
# get all results from https://api-v3.mbta.com/routes then filter locally
# pros:
# - have a full set of results data that we can extend for other functionalities
# cons:
# - most data may not be useful to us and consume local storage
# - if the full data gets updated - change field name or new parameters: we need to update the full data again

# method 2
# Rely on the server API (i.e., https://api-v3.mbta.com/routes?filter[type]=0,1) to filter before results
# are received
# pros:
# - leave the computational work to the api and we get what we need
# - more time and memory efficient if we know what data we need. smaller data set to handle.
# cons:
# - still need to make changes on our end if the data provided by server api do change

# decision:
# question 1, 2, 3 are related to subway routes, so I will take method 2


# solution to question 1
def get_subway_data() -> List[Dict]:
    response = requests.get("https://api-v3.mbta.com/routes?filter[type]=0,1")
    # response.json has two keys: data and jsonapi
    # data is useful
    # data contains a list of 8 subway routes
    return response.json()["data"]


def get_subway_route_long_name() -> set[str]:
    # get long name for all routes
    route_long_names = set()
    for each_subway_route in get_subway_data():
        route_long_names.add(each_subway_route["attributes"]["long_name"])
    return route_long_names


def get_subway_route_id() -> set[Tuple[str, str]]:
    # get all route ids
    route_id = set()  # to store tuple(subway_route_long_name, subway_route_id)
    for each_subway_route in get_subway_data():
        route_id.add((each_subway_route["attributes"]["long_name"], each_subway_route["id"]))
    return route_id


def get_subway_route_stops(route_id: str) -> List[Dict]:
    # return a list of stops for the route id
    response = requests.get(f"https://api-v3.mbta.com/stops?filter[route]={route_id}")
    print(f"{response.status_code} get_subway_route_stops")
    return response.json()["data"]


# solution to Question 2
def list_subway_route_stops(show_max=True) -> Tuple[str, str]:
    # return a tuple of (number of stops, subway route) that has the most or least stops
    subway_stops_count = []
    for each_route_id in get_subway_route_id():
        subway_stops_count.append((len(get_subway_route_stops(each_route_id[1])), each_route_id[0]))
    output = sorted(subway_stops_count)[-1] if show_max else sorted(subway_stops_count)[0]
    print(f"Subway route with most stops: {output}" if show_max else f"Subway route with least stops: {output}")


def show_subway_route(from_station_name: str, to_station_name: str):
    # get all station names
    station_names = {}
    for route_name, route_id in get_subway_route_id():
        print(route_name)
        station_names[route_name] = [
            get_subway_route_stops(route_id)[index]["attributes"]["name"] for index in range(len(get_subway_route_stops(route_id)))
        ]
    pprint(station_names)
    exit
    # check validity of subway route id inputs
    if from_station_name is to_station_long_name:
        raise ValueError(f"From: {from_station_name} and TO: {to_station_long_name} cannot be identical.")
    if from_station_name not in []:
        raise ValueError(f"{from_station_name} does not exist. Please verify station name.")
    if to_station_name not in []:
        raise ValueError(f"{to_station_name} does not exist. Please verify station name.")

    # handle = more than one possible route

    # map stop long name to stop id
    from_station_id = get_subway_route_id()[from_station_name]
    to_station_id = get_subway_route_id()[to_station_name]

    # get subway route information
    from_response = requests.get(f"https://api-v3.mbta.com/routes?filter[type]=0,1&filter[stop]={from_station_id}")
    to_response = requests.get(f"https://api-v3.mbta.com/routes?filter[type]=0,1&filter[stop]={to_station_id}")

    # extract subway route long name
    from_route_data = from_response.json()["data"]
    to_route_data = to_response.json()["data"]
    from_route = [
        from_route_data[index]["attributes"]["long_name"] for index in len(from_route_data)["attributes"]["long_name"]
    ]
    to_route = [
        to_route_data[index]["attributes"]["long_name"] for index in len(to_route_data)["attributes"]["long_name"]
    ]

    # get symmetric difference of from_route and to_route (A union B - A intersection B)
    route_set = set()
    route_set.update(from_route)
    route_set.update(to_route)

    return route_set

from pprint import pprint
# pprint(get_subway_route_stops("Orange")[-7])
pprint(get_subway_route_stops("Red")[4])
pprint(show_subway_route("Central Station", "North Station"))
# pprint("Green-E" in [route_id for long_name, route_id in get_subway_route_id()])
# pprint(get_subway_route_stops("Orange")[0])
# response_source = requests.get("https://api-v3.mbta.com/routes?filter[type]=0,1&filter[stop]=place-north")
 # arlington station
# response_destination = requests.get("https://api-v3.mbta.com/routes?filter[type]=0,1&filter[stop]=place-cntsq")
 # ashmont station
# print(response_source.json()["data"][0]["attributes"]["long_name"])
# print(response_destination.json()["data"][0]["attributes"]["long_name"])

# pprint(get_subway_route_stops("Green-B"))
# print(get_subway_route_id())
# {('Green Line E', 'Green-E'), ('Green Line C', 'Green-C'), ('Mattapan Trolley', 'Mattapan'), ('Blue Line', 'Blue'), ('Orange Line', 'Orange'), ('Green Line B', 'Green-B'), ('Red Line', 'Red'), ('Green Line D', 'Green-D')}
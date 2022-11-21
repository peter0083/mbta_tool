import requests
from typing import List, Dict, Tuple
from functools import lru_cache

# question 1:
#
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
# - API limit is a bottleneck if I need to make many calls for some requirements

# decision:
# question 1, 2, 3 are related to subway routes, so I will take method 2


# solution to question 1
# use caching to reduce api calls
# I use python built-in lru_cache because I do not expect the number of lines to change very often
@lru_cache(maxsize=1)
def get_subway_data() -> List[Dict]:
    response = requests.get("https://api-v3.mbta.com/routes?filter[type]=0,1")
    # response.json has two keys: data and jsonapi
    # data contains a list of 8 subway routes
    return response.json()["data"]


@lru_cache(maxsize=1)
def get_subway_route_long_name() -> set[str]:
    # get long name for all routes
    route_long_names = set(subway_route["attributes"]["long_name"] for subway_route in get_subway_data())
    return route_long_names


@lru_cache(maxsize=1)
def get_subway_route_id() -> set[Tuple[str, str]]:
    # get all route ids
    route_id = set(
        (subway_route["attributes"]["long_name"], subway_route["id"])
        for subway_route in get_subway_data()
    )  # to store tuple(subway_route_long_name, subway_route_id)
    return route_id


@lru_cache(maxsize=8)  # max number of 8 subway lines
def get_subway_route_stops(route_id: str) -> List[Dict]:
    # return a list of stops for the route id
    response = requests.get(f"https://api-v3.mbta.com/stops?filter[route]={route_id}")
    return response.json()["data"]


# solution to Question 2
def list_subway_route_stops(show_max=True) -> Tuple[str, str]:
    # return a tuple of (number of stops, subway route) that has the most or least stops
    subway_stops_count = [
        (len(get_subway_route_stops(route_id[1])), route_id[0]) for route_id in get_subway_route_id()
    ]
    output = sorted(subway_stops_count)[-1] if show_max else sorted(subway_stops_count)[0]
    print(f"Subway route with most stops: {output}" if show_max else f"Subway route with least stops: {output}")


# solution to question 3
@lru_cache(maxsize=20)  # set limit = 20 to reflect api limit
def show_subway_route(from_station_name: str, to_station_name: str):
    # get all station names
    station_names = {}
    route_name_id = get_subway_route_id()
    from_station_id, to_station_id = None, None
    for route_name, route_id in route_name_id:
        raw_stops_data_per_route = get_subway_route_stops(route_id)
        stop_names = []
        for stop in raw_stops_data_per_route:
            stop_name = stop["attributes"]["name"]
            stop_names.append(stop_name)

            # map from_station name to id
            if from_station_name == stop_name:
                from_station_id = stop["id"]
            # map to_station name to id
            if to_station_name == stop_name:
                to_station_id = stop["id"]

        station_names[route_name] = stop_names

    all_stops_name = set()
    for route, stop in station_names.items():
        all_stops_name.update(stop)

    # check validity of subway route id inputs
    if not from_station_id:
        raise ValueError(f"{from_station_name} does not have a matching station ID.")
    if not to_station_id:
        raise ValueError(f"{to_station_name} does not have a matching station ID.")
    if from_station_name == to_station_name:
        raise ValueError(f"From: {from_station_name} and TO: {to_station_name} cannot be identical.")
    if from_station_name not in all_stops_name:
        raise ValueError(f"{from_station_name} does not exist. Please verify station name.")
    if to_station_name not in all_stops_name:
        raise ValueError(f"{to_station_name} does not exist. Please verify station name.")

    # get subway route information per station
    from_response = requests.get(f"https://api-v3.mbta.com/routes?filter[type]=0,1&filter[stop]={from_station_id}")
    to_response = requests.get(f"https://api-v3.mbta.com/routes?filter[type]=0,1&filter[stop]={to_station_id}")

    # extract subway route long name
    from_route_data = from_response.json()["data"]
    to_route_data = to_response.json()["data"]

    from_route = [from_route_data[index]["attributes"]["long_name"] for index in range(len(from_route_data))]
    to_route = [to_route_data[index]["attributes"]["long_name"] for index in range(len(to_route_data))]

    # get symmetric difference of from_route and to_route (A union B - A intersection B)
    # handle multiple possible routes by taking the first route to model take-home prompt example
    route_plan = set()
    route_plan.add(from_route[0])
    route_plan.add(to_route[0])

    return route_plan


# driver code below
# from pprint import pprint

# pprint(get_subway_route_stops("Orange")[-7])
# pprint(get_subway_route_stops("Red")[4])
# pprint(show_subway_route("Central", "North Station"))
# pprint(show_subway_route("Davis", "Kendall/MIT"))
# pprint(show_subway_route("Ashmont", "Arlington"))
# pprint("Green-E" in [route_id for long_name, route_id in get_subway_route_id()])
# pprint(get_subway_route_stops("Orange")[0])
# response_source = requests.get("https://api-v3.mbta.com/routes?filter[type]=0,1&filter[stop]=place-north")
# response_destination = requests.get("https://api-v3.mbta.com/routes?filter[type]=0,1&filter[stop]=place-cntsq")
# print(response_source.json()["data"][0]["attributes"]["long_name"])
# print(response_destination.json()["data"][0]["attributes"]["long_name"])
# pprint(get_subway_route_long_name())

# pprint(get_subway_route_stops("Green-B"))
# print(get_subway_route_id())
# {('Green Line E', 'Green-E'), ('Green Line C', 'Green-C'), ('Mattapan Trolley', 'Mattapan'), ('Blue Line', 'Blue'), ('Orange Line', 'Orange'), ('Green Line B', 'Green-B'), ('Red Line', 'Red'), ('Green Line D', 'Green-D')}

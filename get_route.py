from pprint import pprint

import requests
from typing import List, Dict

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


def get_subway_route_id() -> set[str]:
    # get all route ids
    route_id = set()
    for each_subway_route in get_subway_data():
        route_id.add(each_subway_route["id"])
    return route_id


def get_subway_route_stops(id: str) -> List[Dict]:
    # return a list of stops for the route id
    response = requests.get(f"https://api-v3.mbta.com/stops?filter[route]={id}")
    return response.json()["data"]


def get_subway_route_most_stops() -> Tuple(str, str):
    # return a tuple of (subway route, number of stops) that has the most stops
    subway_stops_count = []
    subway_route_long_name = get_subway_route_long_name()
    subway_route_id = get_subway_route_id()
    for each_route_id in subway_route_id:



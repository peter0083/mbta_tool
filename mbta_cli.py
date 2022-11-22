import argparse
import get_route
from pprint import pprint
import logging
import sys


def main(args=sys.argv[1:]) -> int:
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(prog="mbta_tool", description="simple cli tool to call mbta api")
    if not args or (args and (args[0].startswith("-h") or args[0].startswith("--help"))):
        # if using -h or --help, all arguments should be displayed
        parser.add_argument("-ls_routes", "--list_subway_routes", action="store_true",
                            help="List all subway routes.")
        parser.add_argument("-ls_route_ids", "--list_subway_route_ids", action="store_true",
                            help="List all subway routes and their IDs.")
        parser.add_argument("from_station", type=str, help="Show route from station A to station B.")
        parser.add_argument("to_station", type=str, help="Show route from station A to station B.")

        args1 = parser.parse_args()

    elif args and (args[0].startswith("-") or args[0].startswith("--")):
        # if using optional arguments only
        parser.add_argument("-ls_routes", "--list_subway_routes", action="store_true",
                            help="List all subway routes.")
        parser.add_argument("-ls_route_ids", "--list_subway_route_ids", action="store_true",
                            help="List all subway routes and their IDs.")
        args2 = parser.parse_args()

        if args2.list_subway_route_ids:
            pprint(get_route.get_subway_route_id())
        if args2.list_subway_routes:
            pprint(get_route.get_subway_route_long_name())

    else:
        # using subway route planning
        parser.add_argument("from_station", type=str, help="Show route from station A to station B.")
        parser.add_argument("to_station", type=str, help="Show route from station A to station B.")
        args3 = parser.parse_args()

        if args3.from_station and args3.to_station:
            pprint(get_route.show_subway_route(args3.from_station, args3.to_station))

    return 0


if __name__ == "__main__":
    main()


import argparse
import get_route
from pprint import pprint
import logging


def main() -> int:
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(prog="mbta_tool", description="simple cli tool to call mbta api")
    parser.add_argument("-ls_routes", "--list_subway_routes", action="store_true",
                        help="List all subway routes.")
    parser.add_argument("-ls_route_ids", "--list_subway_route_ids", action="store_true",
                        help="List all subway routes and their IDs.")
    parser.add_argument("from_station", type=str, help="Show route from station A to station B.")
    parser.add_argument("to_station", type=str, help="Show route from station A to station B.")
    args = parser.parse_args()

    if args.list_subway_routes:
        pprint(get_route.get_subway_route_long_name())
    if args.list_subway_route_ids:
        pprint(get_route.get_subway_route_id())
    if args.from_station and args.to_station:
        pprint(get_route.show_subway_route(args.from_station, args.to_station))

    return 0


if __name__ == "__main__":
    main()


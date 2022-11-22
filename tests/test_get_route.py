import get_route
from unittest.mock import Mock, patch
import pytest
from mock_objects import mock_subway_data, mock_route_response_json, mock_stop_response_json, \
    expected_route_response_json, expected_route_stops_json, get_subway_route_stops_side_effect_function, \
    mock_all_station_names


@patch("get_route.requests.get")
def test_get_subway_data(mocked_get):
    mocked_get.return_value.json.return_value = mock_route_response_json
    assert get_route.get_subway_data() == expected_route_response_json


@patch("get_route.get_subway_data")
def test_get_subway_route_long_name(mocked_function):
    expected = {
        'Mattapan Trolley', 'Orange Line', 'Red Line',
        'Green Line C', 'Green Line E', 'Green Line B', 'Green Line D', 'Blue Line'
    }
    mocked_function.return_value = mock_subway_data
    get_subway_data = mocked_function
    assert get_route.get_subway_route_long_name() == expected


@patch("get_route.requests")
def test_get_subway_route_id(mocked_get):
    expected = {
        ('Blue Line', 'Blue'),
        ('Green Line B', 'Green-B'),
        ('Green Line C', 'Green-C'),
        ('Green Line D', 'Green-D'),
        ('Green Line E', 'Green-E'),
        ('Mattapan Trolley', 'Mattapan'),
        ('Orange Line', 'Orange'),
        ('Red Line', 'Red')
    }
    mocked_get.return_value = Mock(
        status_code=200,
        json=mock_stop_response_json
    )
    assert get_route.get_subway_route_id() == expected


@patch("get_route.requests.get")
def test_get_subway_route_stops(mocked_get):
    mocked_get.return_value.json.return_value = mock_stop_response_json
    assert get_route.get_subway_route_stops("Mattapan") == expected_route_stops_json


def test_list_subway_route_stops():
    expected_max = "Subway route with most stops: (25, 'Green Line D')"
    expected_min = "Subway route with least stops: (8, 'Mattapan Trolley')"
    with patch(
            "get_route.get_subway_route_stops",
            side_effect=get_subway_route_stops_side_effect_function
    ) as route_stop_mock, patch(
        "get_route.get_subway_route_id"
    ) as route_id_mock:
        route_id_mock.return_value = {
            ('Blue Line', 'Blue'),
            ('Green Line B', 'Green-B'),
            ('Green Line C', 'Green-C'),
            ('Green Line D', 'Green-D'),
            ('Green Line E', 'Green-E'),
            ('Mattapan Trolley', 'Mattapan'),
            ('Orange Line', 'Orange'),
            ('Red Line', 'Red'),
        }
        assert get_route.list_subway_route_stops(show_max=True) == expected_max
        assert get_route.list_subway_route_stops(show_max=False) == expected_min


def test_get_all_subway_station_names():
    expected_all_station_names = mock_all_station_names

    with patch(
            "get_route.get_subway_route_stops",
            side_effect=get_subway_route_stops_side_effect_function
    ) as route_stop_mock:
        assert get_route.get_all_subway_station_names(None, None) == (expected_all_station_names, None, None)
        assert get_route.get_all_subway_station_names("Ashmont", "Arlington") == (
            expected_all_station_names,
            "place-asmnl",
            "place-armnl"
        )


def test_show_subway_route():
    with patch("get_route.get_all_subway_station_names") as all_station_names_mock:
        all_station_names_mock.return_value = (
            mock_all_station_names,
            None,
            None
        )

        with pytest.raises(ValueError, match=r"None and None do not have matching station IDs."):
            get_route.show_subway_route(None, None)

        all_station_names_mock.return_value = (
            mock_all_station_names,
            "place-asmnl",
            "place-armnl"
        )
        expected_route_set1 = {"Red Line", "Green Line B"}
        assert get_route.show_subway_route("Ashmont", "Arlington") == expected_route_set1

        all_station_names_mock.return_value = (
            mock_all_station_names,
            "place-davis",
            "place-knncl"
        )
        expected_route_set2 = {"Red Line"}
        assert get_route.show_subway_route("Davis", "Kendall/MIT") == expected_route_set2

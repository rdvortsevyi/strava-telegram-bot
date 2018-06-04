import os
import sys
sys.path.append(os.getcwd())

import strava_statistics
from configs import endpoints
import requests
import unittest
from unittest import mock


ATHLETE_INFO = 'ATHLETE_INFO'

TEST_USER = {
    'id': '12345',
    'username': 'test_name',
    'email': 'test_email@test.com'
}

ATHLETE_STAT = {
    'ytd_ride_totals':
    {
        'count': 21,
        'distance': 285000,
        'elevation_gain': 4500
    },
    'all_ride_totals': {
        'count': 85,
        'distance': 3475000,
        'elevation_gain': 35000
    },
    'biggest_ride_distance': 150000
}


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == endpoints.ATHLETE_URL:
        return MockResponse(TEST_USER, 200)
    elif args[0] == endpoints.ATHLETE_STATISTICS_URL % 12345:
        return MockResponse(ATHLETE_STAT, 200)

    return MockResponse(None, 404)


class TestStatistics(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ['STRAVA_TOKEN'] = 'TEST'

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_get_athlete_info(self, mock_get):
        athlete_id = strava_statistics.get_athlete_info()
        self.assertEqual(athlete_id['id'], TEST_USER['id'])

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_all(self, mock_get):
        result = strava_statistics.all()

        this_year = ATHLETE_STAT['ytd_ride_totals']
        all_time = ATHLETE_STAT['all_ride_totals']

        expected_result = ("<b>This year:</b>\n"
                           f"Rides: {this_year['count']}\n"
                           f"Distance: {this_year['distance'] / strava_statistics.METERS_PER_KILOMETER:.1f} km\n"
                           f"Elev Gain: {this_year['elevation_gain']:,d} m\n\n"
                           "<b>All-Time:</b>\n"
                           f"Rides: {all_time['count']}\n"
                           f"Distance: {all_time['distance'] / strava_statistics.METERS_PER_KILOMETER:,.1f} km\n"
                           f"Elev Gain: {all_time['elevation_gain']:,d} m\n"
                           f"Biggest Ride: {ATHLETE_STAT['biggest_ride_distance'] / strava_statistics.METERS_PER_KILOMETER:,.1f} km\n")
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()

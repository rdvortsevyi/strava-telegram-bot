import configs.config as config
import configs.endpoints as endpoints
import requests
from datetime import datetime, timedelta

METERS_PER_KILOMETER = 1000
ERROR_MSG = 'The server error has occurred.'


def get_statistics(criteria):
    """
    Returns statistics based on the given criteria.    
    Criteria can be 'day', 'week', 'month' or 'all'.
    """
    return {
        'day': daily,
        'week': weekly,
        'month': monthly,
        'all': all
    }.get(criteria, None)()


def daily():
    """Returns statistics for this day"""
    start_date = datetime.today().replace(hour=0, minute=0, second=0)
    end_date = datetime.today()

    return _request_data(start_date, end_date, f'day - {start_date:%d %B %Y}')


def weekly():
    """Returns statistics for this week"""
    start_date = datetime.today().replace(hour=0, minute=0, second=0) - \
        timedelta(days=datetime.today().weekday() - 1)
    end_date = datetime.today()

    return _request_data(start_date, end_date, 'week')


def monthly():
    """Returns statistics for this month"""
    start_date = datetime.today().replace(day=1, hour=0, minute=0, second=0)
    end_date = datetime.today()

    return _request_data(start_date, end_date, f'{start_date:%B}')


def all():
    """Returns all statistics for current athlete"""
    try:
        athlete_id = get_athlete_info()['id']

        athlete_stat = requests.get(endpoints.ATHLETE_STATISTICS_URL % athlete_id,
                                    {'access_token': config.get_strava_token()}).json()
    except Exception as e:
        print(e)
        return ERROR_MSG
    else:
        try:
            this_year = athlete_stat['ytd_ride_totals']
            all_time = athlete_stat['all_ride_totals']

            result_str = ("<b>This year:</b>\n"
                          f"Rides: {this_year['count']}\n"
                          f"Distance: {this_year['distance'] / METERS_PER_KILOMETER:.1f} km\n"
                          f"Elev Gain: {this_year['elevation_gain']:,d} m\n\n"
                          "<b>All-Time:</b>\n"
                          f"Rides: {all_time['count']}\n"
                          f"Distance: {all_time['distance'] / METERS_PER_KILOMETER:,.1f} km\n"
                          f"Elev Gain: {all_time['elevation_gain']:,d} m\n"
                          f"Biggest Ride: {athlete_stat['biggest_ride_distance'] / METERS_PER_KILOMETER:,.1f} km\n")
        except Exception as e:
            print(e)
            return ERROR_MSG
        else:
            return result_str


def get_athlete_info():
    """Returns all information about current athlete"""
    try:
        result = requests.get(endpoints.ATHLETE_URL,
                              {'access_token': config.get_strava_token()})
    except Exception as e:
        raise e
    else:
        return result.json()


def _request_data(start_date, end_date, criteria):
    try:
        activities = requests.get(endpoints.ATHLETE_ACTIVITIES_URL, {
                                      'access_token': config.get_strava_token(),
                                      'after': start_date.timestamp(),
                                      'before': end_date.timestamp()
                                  }).json()
    except Exception as e:
        print(e)
        return ERROR_MSG
    else:
        if activities:
            result = {key: sum(item[key] for item in activities)
                      for key in ['distance', 'total_elevation_gain', 'average_speed']}
            
            result['activities_count'] = len(activities)

            try:
                result_str = (f"Statistics for this {criteria}\n"
                              f"Rides: {result['activities_count']}\n"
                              f"Distance: {result['distance'] / METERS_PER_KILOMETER:.2f} km\n"
                              f"Elev Gain: {result['total_elevation_gain']:.1f} m\n"
                              f"Average speed: {result['average_speed'] * 3.6 / result['activities_count']:.1f} km/h")
            except Exception as e:
                print(e)
                return ERROR_MSG
            else:
                return result_str
        else:
            return f'There\'s no data available for the chosen period - {criteria}.'

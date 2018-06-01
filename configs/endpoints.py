# ENDPOINTS
STRAVA_BASE_URL = 'https://www.strava.com/api/v3'

# GET /activities/{id}
# id - id of the activity.
ACTIVITIES_URL = f'{STRAVA_BASE_URL}/activities'

# GET /athlete/activities?after={timestamp}&before={timestamp}&page={int}&per_page={int}
# after - An epoch timestamp to use for filtering activities that have taken place after a certain time.
# before -	An epoch timestamp to use for filtering activities that have taken place before a certain time.
ATHLETE_ACTIVITIES_URL = f'{STRAVA_BASE_URL}/athlete/activities'

# GET /athlete
# Returns the currently authenticated athlete.
ATHLETE_URL = f'{STRAVA_BASE_URL}/athlete'

# GET /athletes/{id}/stats
# id - id of the athlete.
ATHLETE_STATISTICS_URL = f'{STRAVA_BASE_URL}/athletes/%s/stats'

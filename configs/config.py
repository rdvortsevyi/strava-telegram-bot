import json
import os


def load():
    if os.path.isfile('config.json'):
        with open('config.json', 'r') as f:
            json_content = json.load(f)

            os.environ['STRAVA_TOKEN'] = json_content['STRAVA_TOKEN']
            os.environ['TELEGRAM_TOKEN'] = json_content['TELEGRAM_TOKEN']


def get_strava_token():
    return os.environ['STRAVA_TOKEN']


def get_telegram_token():
    return os.environ['TELEGRAM_TOKEN']

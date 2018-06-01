import os
import sys
sys.path.append(os.getcwd())

import unittest
import configs.config as config


STRAVA_TEST_TOKEN = 'STRAVA_TEST_TOKEN'
TELEGRAM_TEST_TOKEN = 'TELEGRAM_TEST_TOKEN'


class ConfigTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ['STRAVA_TOKEN'] = STRAVA_TEST_TOKEN
        os.environ['TELEGRAM_TOKEN'] = TELEGRAM_TEST_TOKEN

    def test_get_strava_token(self):
        case = config.get_strava_token()
        self.assertEqual(case, STRAVA_TEST_TOKEN)

    def test_get_telegram_token(self):
        case = config.get_telegram_token()
        self.assertEqual(case, TELEGRAM_TEST_TOKEN)


if __name__ == '__main__':
    unittest.main()

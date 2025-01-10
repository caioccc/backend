import os

import requests

ACCESS_KEY_WEATHERSTACK = os.environ.get('ACCESS_KEY_WEATHERSTACK', default='eb2aac3066ce60e74c44dab051fc232d')


def get_weather(city, code):
    url = 'https://api.weatherstack.com/current?access_key={ACCESS_KEY_WEATHERSTACK}'.format(
        ACCESS_KEY_WEATHERSTACK=ACCESS_KEY_WEATHERSTACK)
    querystring = {"query": "{CITY},{CODE}".format(CITY=city, CODE=code)}
    response = requests.get(url, params=querystring)
    return response.json()

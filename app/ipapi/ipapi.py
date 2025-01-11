import os

import requests

ACCESS_KEY_IPSTACK = os.environ.get('ACCESS_KEY_IPSTACK', default='a0a99b4657e1c9c998b2d40f8f2548a0')


def get_ip_full_data():
    url = "https://api.ipstack.com/check?access_key={ACCESS_KEY_IPSTACK}".format(ACCESS_KEY_IPSTACK=ACCESS_KEY_IPSTACK)
    response = requests.get(url)
    return response.json()

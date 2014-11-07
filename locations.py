import os
import json
import threetaps
import urllib2, requests
import re
from bs4 import BeautifulSoup

client = threetaps.Threetaps('b1b0f839c5542506ae18ef66b6679299')
json_return = client.reference.locations('city', params={'metro': 'USA-BOS'})

locations = json_return['locations']
city_codes = []

for location in locations:
    if "MA" in location['full_name']:
        if location['short_name'] == "Boston":
            city_codes.append(location['code'])
        elif location['short_name'] == "Cambridge":
            city_codes.append(location['code'])
        elif location['short_name'] == "Somerville":
            city_codes.append(location['code'])
        elif location['short_name'] == "Newton":
            city_codes.append(location['code'])
        elif location['short_name'] == "Brookline":
            city_codes.append(location['code'])
        elif location['short_name'] == "Watertown":
            city_codes.append(location['code'])
        elif location['short_name'] == "Chelsea":
            city_codes.append(location['code'])
        elif location['short_name'] == "Revere":
            city_codes.append(location['code'])
        elif location['short_name'] == "Quincy":
            city_codes.append(location['code'])
        elif location['short_name'] == "Milton":
            city_codes.append(location['code'])
        elif location['short_name'] == "Dedham":
            city_codes.append(location['code'])
        elif location['short_name'] == "Everett":
            city_codes.append(location['code'])
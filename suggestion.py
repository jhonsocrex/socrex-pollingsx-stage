import os
import json
import threetaps
import urllib2, requests
import re
from bs4 import BeautifulSoup
from pymongo import MongoClient
from bson.json_util import dumps

def pretty_print(jsondata):

    print json.dumps(jsondata, sort_keys=True, indent=4, separators=(',', ': '))

def bson_print(bsondata):

    print dumps(bsondata, sort_keys=True, indent=4, separators=(',', ': '))

client = threetaps.Threetaps('b1b0f839c5542506ae18ef66b6679299')

MONGO_URL = os.environ.get('MONGOHQ_URL')

dbclient = MongoClient(MONGO_URL)
db = dbclient['app30172457']
db_listings = db.listings

#all_listings = listings.listings

#print len(all_listings)


user_pad = dict()
user_pad['upper_price'] = 2000
user_pad['lower_price'] = 1000
user_pad['bedroom'] = 1
user_pad['bathroom'] = 1


#pretty_print(user_pad)
count = 0

for listing in db_listings.find():
    #if user_pad['lower_price'] <= listing['price'] <= user_pad['upper_price']:
    bson_print(listing)
    count = count +1

print count

errors = []
results = {}
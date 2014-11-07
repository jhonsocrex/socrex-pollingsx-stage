
import os
import json
import threetaps
import urllib2, requests
import re
import time
import datetime
import traceback

from pymongo import MongoClient
from bs4 import BeautifulSoup
import locations
from apscheduler.schedulers.blocking import BlockingScheduler
from bson.objectid import ObjectId

from business.implementations.implementations import Implementations

from persistence.collections.neighborhoods import Neighborhoods

from threading import Thread

import logging

from mlsscraperlauncher import MLSScraperLauncher





client = threetaps.Threetaps('b1b0f839c5542506ae18ef66b6679299')
anchor = ""
MONGOHQ_URL = 'mongodb://heroku:JPbXJfkZ1Zm2nJ7P-GD7AR12oj10-dsZ6iZyaxYI67THwWeVVeaSHPqEaPXKfeSNVZc86TVtdplQmMc_DkoL2w@kahana.mongohq.com:10066/app30172457'
#MONGO_URL = os.environ.get('MONGOHQ_URL')
dbclient = MongoClient(MONGOHQ_URL)
db = dbclient['app30172457']
db_listings = db.listings
newImplementation = Implementations()

def pretty_print(jsondata):

    print json.dumps(jsondata, sort_keys=True, indent=4, separators=(',', ': '))

def get_month(month):
    if month is "jan":
        return "01"
    elif month is "feb":
        return "02"
    elif month is "mar":
        return "03"
    elif month is "apr":
        return "04"
    elif month is "may":
        return "05"
    elif month is "jun":
        return "06"
    elif month is "jul":
        return "07"
    elif month is "aug":
        return "08"
    elif month is "sep":
        return "09"
    elif month is "oct":
        return "10"
    elif month is "nov":
        return "11"
    elif month is "dec":
        return "12"

def updateNeighborhoodInfo(listingid, neighborhoodsCoords):
    newImplementation.updateNeighborhoodInfo(listingid, neighborhoodsCoords)
    
def getNeighborhoodCoords():
    neighborhoodCollectionPersistence = Neighborhoods(db)
        # get all neighborhoods coords
    neighborhoodsCoords = neighborhoodCollectionPersistence.getNeighborhoodsCoords()
    return neighborhoodsCoords
    
def poll():
    try:
        utc_dt = datetime.datetime.now()
        print utc_dt
        global anchor
        anchor_result = client.polling.poll(params={'location.city': locations.city_codes[0], 'source': 'CRAIG', 'category': 'RHFR', 'anchor': anchor})
        anchor = anchor_result["anchor"]
        postings = anchor_result["postings"]
        
        # get all neighborhoods coords
        neighborhoodsCoords = getNeighborhoodCoords()
        
        for post in postings:
            external_url = requests.get(post['external_url'])
            soup = BeautifulSoup(external_url.text)
            address = soup.find(class_="mapaddress")
            if (address is not None) and len(address) == 1:
                print "post" , post
                # Get base apartment information
                title =  soup.find(class_="postingtitle").text
                print title
                print post['external_url']
    
                price_re = re.search('\$\d+',title)
                price =  price_re.group(0)[1:]
                annotations = post["annotations"]
                bedroom = annotations["bedrooms"][:1]
                bathroom = annotations["bathrooms"][:1]
                feetype = annotations["source_subcat"]
    
                # Check for repeated entries
    
                #data = db_listings.find().sort({"_id":-1}).limit(250)
                data = db_listings.find().sort([("_id", -1)]).limit(250)
                
                
                all_data = list(data)
                repeated = False
                add = address.get_text()
                print "all_data" , all_data
                print "for init"
                for element in all_data:
                    if element["address"] in add or add in element["address"]:
                        if element["price"] == int(price) and element["bedroom"] == int(bedroom) and element["bathroom"] == int(bathroom):
                            repeated = True
                            print "Repeat"
                            break
                print "for end"
                print "repeated", repeated
    
    
                if not repeated:
                    print "inside not repeated"
                    # Get image links
                    thumbs = soup.find(id="thumbs")
                    pictures = []
                    for child in thumbs.children:
                        pictures.append(child['href'])
    
                    # Process move-in date (this should be optimized)
    
                    move_in = annotations["available"]
                    if len(move_in) < 6:
                        month = get_month(move_in[:3])
                        day = entry[4:]
                        if len(day) == 1:
                            "0"+day
                        if int(month) < datetime.date.today().month-3:
                            year = datetime.date.today().year + 1
                        else:
                            year = datetime.date.today().year
                        move_in_date = str(year)+day+month
                    else:
                        day = str(datetime.date.today().day)
                        if len(day) == 1:
                            day = "0"+day
                        month = str(datetime.date.today().month)
                        if len(month) == 1:
                            month = "0"+month
                        year = str(datetime.date.today().year)
                        move_in_date = year+day+month
    
                    # Create listing dictionary
    
                    listing = dict()
                    listing['body'] = soup.find(id="postingbody").get_text()
                    listing['title'] = title
                    listing['description'] = soup.meta.meta['content']
                    listing['url'] = post['external_url']
                    listing['lastupdated'] = soup.find(class_="postinginfo").time['datetime']
                    listing['address'] = address.get_text()
                    listing['longitude'] = float(soup.find(id="map")['data-longitude'])
                    listing['latitude'] = float(soup.find(id="map")['data-latitude'])
                    listing['price'] = int(price)
                    listing['bedroom'] = int(bedroom)
                    listing['bathroom'] = int(bathroom)
                    listing['feetype'] = feetype
                    listing['move_in'] = move_in_date
                    listing['pictures'] = pictures
                    # pretty_print(listing)
    
                    # Insert into DB
                    listing_id = db_listings.insert(listing)
                    print "listing_id",  listing_id
                    t = Thread(target=updateNeighborhoodInfo, args=(listing_id,neighborhoodsCoords,))
                    t.start()
                    
    except Exception as e:
        print "there was an exeption in the poll method"            
        print str(e)   
        print traceback.format_exc()


def setup_crawler(domain):
    spider = MLSSpider(domain=domain)
    settings = get_project_settings()
    crawler = Crawler(settings)
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()
        
def run_spiders():
    for domain in ['themlsonline.com']:
        setup_crawler(domain)
    log.start()
    reactor.run()

## craiglist data pull
if __name__ == '__main__':
    
    scheduler = BlockingScheduler()
    anchor_result = client.polling.poll(params={'location.city': locations.city_codes[0], 'source': 'CRAIG', 'category': 'RHFR'})
    anchor = anchor_result["anchor"]

    scheduler.add_job(poll, 'interval', seconds=30)
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        logging.basicConfig()
        scheduler.start()
        #poll()
    except (KeyboardInterrupt, SystemExit, Exception) as e:
        print str(e)
        print traceback.format_exc()



## start themlsonline pull
"""
if __name__ == '__main__':
    
    try:
        
        # get all neighborhoods coords
        neighborhoodsCoords = getNeighborhoodCoords()
        # run mls spider
        mslLauncher = MLSScraperLauncher()
        mslLauncher.run_spiders(neighborhoodsCoords)
        
    except (KeyboardInterrupt, SystemExit, Exception) as e:
        print str(e)
        print traceback.format_exc()
"""
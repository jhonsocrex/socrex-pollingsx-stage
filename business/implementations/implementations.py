
from persistence.mongodatabase import MongoDatabase
from pymongo import MongoClient

from persistence.collections.listings import Listings
from persistence.collections.neighborhoods import Neighborhoods

from pointcalculator import PointCalculator

class Implementations():
    
    def __init__(self):
 
        # load constants
        self.__MONGO_URL__ = "mongodb://heroku:JPbXJfkZ1Zm2nJ7P-GD7AR12oj10-dsZ6iZyaxYI67THwWeVVeaSHPqEaPXKfeSNVZc86TVtdplQmMc_DkoL2w@kahana.mongohq.com:10066/app30172457"
        self.__MONGO_DB__ = "app30172457"
        
        # jhon's dev environment
        #self.__MONGO_URL__ = "mongodb://jhon:jhon@dogen.mongohq.com:10021/app31380057"
        #self.__MONGO_DB__ = "app31380057"

        # init db connection
        self.__myDB__ = MongoDatabase(self.__MONGO_URL__)
        self.__db__ = self.__myDB__.getDB(self.__MONGO_DB__)
        
    def saveScrapedListing(self, listingObject):
        listingCollection = Listings(self.__db__)
        listingid = listingCollection.saveListing(listingObject)
        return listingid
    
    def updateNeighborhoodInfo(self, listingid= None, neighborhoodsCoords=None):
        returnSuccess = False
        
        if listingid is not None and neighborhoodsCoords is not None:
    		
    		listingCollectionPersistence = Listings(self.__db__)
    		neighborhoodCollectionPersistence = Neighborhoods(self.__db__)
    		# get single listing Coords
    		litingsCoords = listingCollectionPersistence.getUnitListingCoordsByListingId(listingid)
    		# implement class that has ANN algorithms
    		newPointCalculator = PointCalculator(litingsCoords, neighborhoodsCoords)
    		# get coords of all the neighbors
    		nearesNeighborhoodArrayCords = newPointCalculator.getNearestPointArrayCoords()
    		# get neighbor based on its coords
    		#nearestNeighborhoodId = neighborhoodCollectionPersistence.getNeighborhoodIdByCoords(nearesNeighborhoodArrayCords[0],nearesNeighborhoodArrayCords[1])
    		nearestNeighborhood = neighborhoodCollectionPersistence.getNeighborhoodByCoords(nearesNeighborhoodArrayCords[0],nearesNeighborhoodArrayCords[1])
    		# uddate listing neighborId
    		#listingCollectionPersistence.updateListingNeighborhoodIdByListingId(listingid,nearestNeighborhoodId)
    		listingCollectionPersistence.updateListingNeighborhoodByListingId(listingid,nearestNeighborhood)
	        
	        returnSuccess = True
	        
        return returnSuccess
    
    def verifyListingAvailability(self, listingid= None, useremail=None ):
        returnSuccess = False
        
        if listingid is not None and useremail is not None:
	        
	        # save hit in the listing option collection
	        listingOptionCollection = ListingOptions(self.__db__)
	        listingOptionCollection.saveListingOptionClick(listingid,useremail,"verifyavailability")
	        
	        returnSuccess = True
	        
        return returnSuccess
    
    def expertReview(self, listingid= None, useremail=None ):
        returnSuccess = False
        
        if listingid is not None and useremail is not None:
	        
	        # save hit in the listing option collection
	        listingOptionCollection = ListingOptions(self.__db__)
	        listingOptionCollection.saveListingOptionClick(listingid,useremail,"expertreview")
	        
	        returnSuccess = True
	        
        return returnSuccess
    
    def virtualTour(self, listingid= None, useremail=None ):
        returnSuccess = False
        
        if listingid is not None and useremail is not None:
	        
	        # save hit in the listing option collection
	        listingOptionCollection = ListingOptions(self.__db__)
	        listingOptionCollection.saveListingOptionClick(listingid,useremail,"virtualtour")
	        
	        returnSuccess = True
	        
        return returnSuccess
        
        
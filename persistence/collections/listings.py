
# mongodb
from pymongo import MongoClient
from bson.objectid import ObjectId


class Listings():
    
    def __init__(self, db):
        self.__collectionName__ = "listings"
        self.__db__ = db
        self.__loadConnection()
    
    def __loadConnection(self):
        self.__collectionObject__ = self.__db__[self.__collectionName__]
        
    def saveListing(self , listingObject):
        objToInsert = listingObject
        listingid = self.__collectionObject__.insert(objToInsert)
        return listingid
        
    def getUnitListingCoordsByListingId(self, listingId):
        returnCoord = None
        if listingId is not None:
            listingObj = self.__collectionObject__.find_one({'_id': ObjectId(listingId)} )
            if listingObj:
                ## from string to float
                returnCoord = [float(listingObj["latitude"]) , float(listingObj["longitude"])]    
        return returnCoord
    
    def updateListingNeighborhoodIdByListingId(self, listingId, neighborhoodId):
        returnValue = False
        if listingId is not None:
            listingObj = self.__collectionObject__.update({'_id': ObjectId(listingId)},{"$set":{'neighborhoodid':ObjectId(neighborhoodId)}} )
            returnValue = True
        return returnValue
    
    def updateListingNeighborhoodByListingId(self, listingId, neighborhoodObj):
        returnValue = False
        if listingId is not None:
            listingObj = self.__collectionObject__.update({'_id': ObjectId(listingId)},{"$set":{'neighborhood':neighborhoodObj}} )
            returnValue = True
        return returnValue
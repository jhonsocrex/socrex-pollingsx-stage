
# mongodb
from pymongo import MongoClient
from bson.objectid import ObjectId


class Neighborhoods():
    
    def __init__(self, db):
        self.__collectionName__ = "hoods"
        self.__db__ = db
        self.__loadConnection()
    
    def __loadConnection(self):
        self.__collectionObject__ = self.__db__[self.__collectionName__]
        
    def getNeighborhoodsCoords(self):
        returnNeighborhoodsCoords = None
        neighborhoodObjs = self.__collectionObject__.find()
        if neighborhoodObjs:
            returnNeighborhoodsCoords = []
            for neighborhoodObj in neighborhoodObjs:
                for coordinate in neighborhoodObj["Coordinates"]:
                    returnNeighborhoodsCoords.append([coordinate['Latitude'] , coordinate['Longitude']])
        return returnNeighborhoodsCoords
    
    def getNeighborhoodIdByCoords(self, latitude, longitude):
        returnId = None
        if latitude is not None and longitude  is not None :
            # modify based on he new structure 
            #shapes: {$elemMatch: {color: "red"}}
            # $in: [latitude, longitude]
            print "latitude" , latitude
            print "longitude" , longitude
            neighborhoodObj = self.__collectionObject__.find_one({ 'Coordinates': { '$elemMatch': {"Latitude": latitude , "Longitude": longitude}} } )
            print "neighborhoodObj" , neighborhoodObj
            if neighborhoodObj:
                returnId = neighborhoodObj["_id"]
        return returnId
    
    def getNeighborhoodByCoords(self, latitude, longitude):
        returnObj = None
        if latitude is not None and longitude  is not None :
            # modify based on he new structure 
            #shapes: {$elemMatch: {color: "red"}}
            # $in: [latitude, longitude]
            print "latitude" , latitude
            print "longitude" , longitude
            neighborhoodObj = self.__collectionObject__.find_one({ 'Coordinates': { '$elemMatch': {"Latitude": latitude , "Longitude": longitude}} } )
            print "neighborhoodObj" , neighborhoodObj
            if neighborhoodObj:
                returnObj = {"_id":neighborhoodObj["_id"] , "Name":neighborhoodObj["Name"]}
        return returnObj
        
# impors for spyder#
import datetime
import scrapy
from scrapy.spider import BaseSpider
from bs4 import BeautifulSoup
from scrapy.http import Request

# imports for implementation
from business.implementations.implementations import Implementations

from threading import Thread

#newImplementation = Implementations()

class MLSSpider(BaseSpider):
    name = "mls"
    allowed_domains = ["themlsonline.com"]
    fileName = None
    fileObject = None
    openFileMode = None
    baseURL = 'http://www.themlsonline.com/MA/Boston/'
    printFlag = False
    newImplementation = Implementations()
    
    """
    start_urls = [
        ## prev
        #"http://www.mlsfinder.com/ma_mlspin/laurarossinow/index.cfm?action=searchresults&searchkey=813cb945-ab8b-9176-bd10-fc391c394065&sr=1",
        "http://www.themlsonline.com/MA/Boston/results,0fa9a4878169b37cd4b8b0ffc2907b76,1.html"
    ]"""
    
    start_urls = ['http://www.themlsonline.com/MA/Boston/results,3b4b7e9757be706512c7425d28668d3e,%s,0.html' % page for page in xrange(1,83)]
    
    def __init__(self, category=None, neighborhoodsCoords=None, *args, **kwargs):
        super(BaseSpider, self).__init__(*args, **kwargs)
        self.neighborhoodsCoords = neighborhoodsCoords
    
    def parse(self, response):
        responseBoody = response.body
        ## saving data in file
        ##self.saveDataInFile(responseBoody)
        ## get listings herfs
        listingsHrefsList = self.getListingsUrlFromText(responseBoody)
        ## call spyders for each link
        for listingsHrefElement in listingsHrefsList:
            yield scrapy.Request(listingsHrefElement, callback=self.parseListingDetailCallback)
        
    def saveDataInFile(self,bodyText):
        
        if self.fileName is None:
            self.fileName = self.name + datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S") + ".txt"
            self.openFileMode = 'wb'
            self.fileObject = open(self.fileName, self.openFileMode)
        elif self.openFileMode != 'a':
                self.openFileMode = 'a' 
                self.fileObject = open(self.fileName, self.openFileMode)
        
        self.fileObject.write(bodyText)
    
    def getListingsUrlFromText(self,bodyText):
        resultList = []
        bodyObject = BeautifulSoup(bodyText)
        findMLSClassResultList = bodyObject.findAll("a", { "class" : "mls" })
        for findMLSClassResultElement in findMLSClassResultList:
            listingURN = findMLSClassResultElement['href']
            listingURL = self.baseURL + listingURN
            resultList.append(listingURL)
        return resultList
        
    def parseListingDetailCallback(self, response):
        print "parseListingDetailCallback"
        responseBody = response.body
        ## saving data in file
        if self.printFlag == True:
            self.saveDataInFile(responseBody)
            self.printFlag == False
        objectToSave = {}
        ## get info from response.body
        bodyObject = BeautifulSoup(responseBody)
        
        objectToSave['address'] = self.getListingAddress(bodyObject)
        objectToSave['title'] = objectToSave['address']
        objectToSave['body'] = self.getListingDescription(bodyObject)
        objectToSave['bathroom'] = self.getListingBedroom(bodyObject)
        objectToSave['bedroom'] = self.getListingBathroom(bodyObject)
        objectToSave['price'] = self.getListingPrice(bodyObject)
        objectToSave['pictures'] = self.getPicturesArray(bodyObject)
        objectToSave['source'] = 'themlsonline'
        objectToSave['url'] = response.url
        ## position
        position = self.getListingPosition(bodyObject)
        objectToSave['latitude'] = position['latitude']
        objectToSave['longitude'] = position['longitude']
        # lastupdated
        objectToSave['lastupdated'] = datetime.datetime.utcnow().isoformat()
        
        
        
        
        
        print "objectToSave" , objectToSave
        
        # save listing in database    
        self.saveListing(objectToSave)
        
        
        
        # detail_data_text
        #BeautifulSoup(detalitDataTableElement).bodyObject.find("div", { "class" : "detail_data_tbl" })
        
        #detail_data_tbl
        
    def saveListing(self, listingObject):
        listingid = self.newImplementation.saveScrapedListing(listingObject)
        towriteindocument = ''
        if isinstance(listingid, str):
            towriteindocument = "is a string : " +listingid
        else:
            towriteindocument = "is not a string, is a  : " + str(type(listingid))
        
        self.saveDataInFile(towriteindocument)
        t = Thread(target=self.updateNeighborhoodInfo, args=(listingid,self.neighborhoodsCoords,))
        t.start()
        
    def updateNeighborhoodInfo(self, listingid, neighborhoodsCoords):
        self.newImplementation.updateNeighborhoodInfo(listingid, neighborhoodsCoords)
    
    def getPicturesArray(self , bodyObject):
            
        returnListingPicturesList = None
        # 
        
        javascriptElements = bodyObject.findAll("script")
        javascriptFunctionElementText = self.getListElementTextByString(javascriptElements , "mort_calc_loaded = false")
        #print "javascriptFunctionElementText" , javascriptFunctionElementText
        lrgsSplitElementsList = javascriptFunctionElementText.split('lrgs[')
        #print "lrgsSplitElementsList" , lrgsSplitElementsList
        ## delete fisrt element of the list
        del lrgsSplitElementsList[0]
        
        picturesList = []
        
        for lrgsSplitElement in lrgsSplitElementsList:
            lrgsSplitArray = lrgsSplitElement.split("'")
            for lrgsSplitElement in lrgsSplitArray:
                #print "lrgsSplitElement" , lrgsSplitElement
                if lrgsSplitElement.startswith( 'http://photos.themlsonline.com' ):
                    picturesList.append(lrgsSplitElement)
                
        returnListingPicturesList = picturesList
                
        return returnListingPicturesList
        
    
    def getListingAddress(self , bodyObject):
            
        returnListingAddress = None
            
        addressElement = bodyObject.find("li", { "class" : "detail_address" })
        countryElement = bodyObject.find("li", { "class" : "detail_county" })
        
        returnListingAddress = addressElement.get_text() + " " + countryElement.get_text()
                
        return returnListingAddress
    
    def getListingDescription(self , bodyObject):
            
        returnListingDescription = None
            
        detailDataTableElement = bodyObject.find("div", { "class" : "detail_data_tbl" })
        detailDataTableTextElementList = detailDataTableElement.findAll("div", { "class" : "detail_data_text" })
        
        for detailDataTableTextElement in detailDataTableTextElementList:
            detailDataTableTextSpanElement = detailDataTableTextElement.find("span", { "style" : "font-size:13px" })
            if detailDataTableTextSpanElement is not None:
                returnListingDescription = detailDataTableTextSpanElement.get_text()
                break
                
        return returnListingDescription
    
    def getListingBathroom(self , bodyObject):
        returnListingInfo = None
        fieldValue = self.getInfoFromListingInformationBox(bodyObject, "Bathrooms")
        valueInt = self.extractIntValueFromString(fieldValue)
        returnListingInfo = valueInt
        return returnListingInfo
        
    def getListingBedroom(self , bodyObject):
            
        returnListingInfo = None
        fieldValue = self.getInfoFromListingInformationBox(bodyObject, "Bedrooms")
        valueInt = self.extractIntValueFromString(fieldValue)
        returnListingInfo = valueInt
        return returnListingInfo
    
    def getListingPosition(self , bodyObject):
            
        returnListingInfo = None
        
        #print "bodyObject" , bodyObject
        javascriptElements = bodyObject.findAll("script")
        javascriptFunctionElementText = self.getListElementTextByString(javascriptElements , "featuredVideo")
        
        ### latitude
        beginLatitudeTextsList = javascriptFunctionElementText.split("lat=")
        beginLatitudeText = beginLatitudeTextsList[1]
        latitudeText = beginLatitudeText.split("&")[0]
        latitudeFloat = float(latitudeText)
        
        ### longitude
        beginLongitudeTextsList = javascriptFunctionElementText.split("lon=")
        beginLongitudeText = beginLongitudeTextsList[1]
        longitudeText = beginLongitudeText.split("'")[0]
        longitudeFloat = float(longitudeText)
        
        
        returnListingInfo = {'latitude':latitudeFloat , 'longitude':longitudeFloat}
        return returnListingInfo
        
    def getListingPrice(self , bodyObject):
            
        returnListingInfo = None
        priceFieldValue = self.getInfoFromListingInformationBox(bodyObject, "List Price")
        priceInt = self.extractIntValueFromString(priceFieldValue)
        returnListingInfo = priceInt
        return returnListingInfo
        
    def extractIntValueFromString(self, stringValue):
        r = stringValue
        s = ''.join(x for x in r if x.isdigit())
        return int(s)
        
    def getListElementTextByString(self, elementList, stringValue):
        return self.getListElementByString(elementList, stringValue).get_text()
    
    def getListElementByString(self, elementList, stringValue):
        # this can be way improved!!!
        aElementsList = elementList
        requestedField = stringValue
        returnListingInfo = None
        
        for aElementsListElement in aElementsList:
            aElementsListElementText = aElementsListElement.get_text()
            if requestedField in aElementsListElementText:
                returnListingInfo = aElementsListElement
                break
            
        return returnListingInfo
    
    def getInfoFromListingInformationBox(self , bodyObject, requestedField):
        returnListingInfo = None
            
        detailDataTableElement = bodyObject.find("div", { "class" : "detail_data_tbl" })
        
        detailDataTableTextElementList = detailDataTableElement.findAll("div", { "class" : "detail_data_text" })
        
        if len(detailDataTableTextElementList) >= 3:
            listingInformationObject = detailDataTableTextElementList[2]
            aElementsList = listingInformationObject.findAll("div", { "class" : "a" })
            
            returnListingInfo = self.getListElementTextByString(aElementsList, requestedField+":")
                
        return returnListingInfo
        





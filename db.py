from pymongo import MongoClient

#client = MongoClient('mongodb://heroku:JPbXJfkZ1Zm2nJ7P-GD7AR12oj10-dsZ6iZyaxYI67THwWeVVeaSHPqEaPXKfeSNVZc86TVtdplQmMc_DkoL2w@kahana.mongohq.com:10066/app30172457')
db = client['app30172457']


listings = db.listings

listings.drop()

# print listings
# listing_id = listings.insert(user_pad)
# print listing_id
import urllib 
import pymongo
uri = "mongodb+srv://VLPSDB:"+ urllib.parse.quote('VLPS@2022') + "@cluster0.otftf.mongodb.net/?retryWrites=true&w=majority"
mongo = pymongo.MongoClient(uri)

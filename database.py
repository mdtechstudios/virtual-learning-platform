import pymongo
import urllib
import certifi

conn_str = "mongodb+srv://admin:"+ urllib.parse.quote('admin')+"@cluster0.otftf.mongodb.net/?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE"
client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000,tlsCAFile=certifi.where())
db = client.db

try:
    # print(client.server_info())
    print("Connected to MongoDB Atlas")
except Exception:
    print("Unable to Connect to the MongoDB Atlas")
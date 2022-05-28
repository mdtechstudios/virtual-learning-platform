import pymongo
import urllib

# Replace the uri string with your MongoDB deployment's connection string.
conn_str = "mongodb+srv://admin:"+ urllib.parse.quote('admin')+"@cluster0.otftf.mongodb.net/?retryWrites=true&w=majority"
# set a 5-second connection timeout
client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)

try:
    # print(client.server_info())
    print("Connected to MongoDB Atlas")
except Exception:
    print("Unable to connect to the MongoDB Atlas")
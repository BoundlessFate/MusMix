from flask import Flask,g
import pymongo
from sha import sha256
import dbConnection

app = Flask(__name__)

client = dbConnection.connect_mongo()
db = client["musmixdata"]
collection = db.userdata
username = "testuser"
password = "111111"
result = collection.find_one({"auth": sha256.generate_hash(username + password).hex()})
if result == None:
    print('username or password incorrect')
else:
    print(result['type'])

'''
client = pymongo.MongoClient("mongodb+srv://MusMixAdmin1:uGpw6A07tp2kbTP7@musmix.bb1xivw.mongodb.net/",
                             username = "MusMixAdmin1", password = "uGpw6A07tp2kbTP7")
db = client["musmixdata"]
collection = db.userdata
username = "testuser"
password = "111111"

result = collection.find_one({"auth": sha256.generate_hash(username + password).hex()})
if result == None:
    print('username or password incorrect')
else:
    print(result['type'])
'''


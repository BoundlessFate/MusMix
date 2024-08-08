from flask import Flask,g
import pymongo
from sha import sha256
import dbConnection

client = pymongo.MongoClient("mongodb+srv://MusMixAdmin1:uGpw6A07tp2kbTP7@musmix.bb1xivw.mongodb.net/",
                             username = "MusMixAdmin1", password = "uGpw6A07tp2kbTP7")
db = client["musmixdata"]
collection = db.userdata
username = "testuser"
password = "111111"
auth = sha256.generate_hash(username + password).hex()
result = collection.update_one({"auth":auth},{'$addToSet': {'favorite_songs': "222"}})

if result.matched_count == 0:
    print("Didn't find user")
elif result.modified_count == 0:
    print("Update failed")
else:
    print("Update success")
'''
favoriteSongs = result.get("favorite_songs", [])
print(favoriteSongs)
if favoriteSongs == None:
    print('username or password incorrect')
else:
    print(1)


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

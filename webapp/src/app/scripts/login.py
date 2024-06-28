import sys
from hashlib import sha256
from pymongo import MongoClient
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64
def generateKey(key):
    newKey = key
    num = 32 - len(key)
    for i in range(0,num):
        newKey += "a"
    return newKey
# 7EfBAgXJBn5xX4PydtZvBw==
n = len(sys.argv)
assert n == 3 # If this fails then the wrong number of args is used
uname = sys.argv[1]
pwd=sys.argv[2]
combined=uname+pwd # combine the uname and pwd
hash = sha256(combined.encode()).hexdigest() # SHA256 hash them
client = MongoClient("mongodb+srv://MusMixAdmin1:uGpw6A07tp2kbTP7@musmix.bb1xivw.mongodb.net/")
db = client.get_database("musmixdata")
collection = db.get_collection("userdata")
document = collection.find_one({"auth": hash})
if document:
    encryptedLastSong = document.get('lastsong')
    ciphertext = base64.b64decode(encryptedLastSong)
    key_bytes = generateKey(pwd).encode('utf-8')
    cipher = AES.new(key_bytes, AES.MODE_ECB)
    decrypted = cipher.decrypt(ciphertext)
    decrypted = unpad(decrypted, AES.block_size)
    decrypted_text = decrypted.decode('utf-8')
    print("Last Song: ", decrypted_text)
else:
    print("Document with auth code "+hash+" not found.")
client.close()
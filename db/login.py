from flask import Flask, request, current_app
import pymongo
from sha import sha256
import dbConnection

app = Flask(__name__)

client = None
collection = None
db = None
with app.app_context():
    db = dbConnection.connect_mongo()
    #db = client["musmixdata"]
    collection = db['userdata']


@app.route('/login', methods=['GET', 'POST'])
def user_login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        auth = sha256.generate_hash(username + password).hex()
        result = collection.find_one({'username': username, 'auth': auth})
        if result == None:
            print("Incorrect username or password")
        else:
            print("Login success")

if __name__ == '__main__':
    app.run(debug=True)

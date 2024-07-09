from flask import Flask, request, jsonify
import pymongo
from sha import sha256
import dbConnection

app = Flask(__name__)

client = None
collection = None
db = None
with app.app_context():
    db = dbConnection.connect_mongo()
    collection = db['userdata']


@app.route('/login', methods=['POST','GET'])
def user_login():
    print(1111)
    if request.method == "POST":
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        auth = sha256.generate_hash(username + password).hex()
        result = collection.find_one({'username': username, 'auth': auth})
        if result is None:
            print("Incorrect username or password")
            return jsonify({"message": "Incorrect username or password"}), 404
        else:
            print("Login success")
            return jsonify({"message": "Login success"}), 200

if __name__ == '__main__':
    app.run(debug=True)

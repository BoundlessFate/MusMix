from flask import Flask, request, jsonify
from flask_cors import CORS
import pymongo
from sha import sha256
import dbConnection

app = Flask(__name__)
CORS(app)

client = None
collection = None
db = None
with app.app_context():
    db = dbConnection.connect_mongo()
    collection = db['userdata']


@app.route('/login', methods=['POST','GET','OPTIONS'])
def user_login():
    print(1111)
    if request.method == "POST":
        print(2222222)
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        print(username)
        print(password)
        auth = sha256.generate_hash(username + password).hex()
        result = collection.find_one({'auth': auth})
        if result is None:
            print("Incorrect username or password")
            return jsonify({"message": "Incorrect username or password"}), 404
        else:
            print("Login success")
            return jsonify({"message": "Login success"}), 200
    if request.method == "OPTIONS":
        # Handle the OPTIONS request
        response = app.make_response('')
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        return response

if __name__ == '__main__':
    app.run(debug=True)

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


@app.route('/register', methods=['POST','GET', 'OPTIONS'])
def user_register():
    print(1111)
    if request.method == "POST":
        print(2222222)
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        print(username)
        print(password)
        auth = sha256.generate_hash(username + password).hex()
        data = {
            'auth': auth
        }
        result = collection.find_one({'auth': auth})
        if result is None:
            # User is not in the system yet, continue with register
            insert_result = collection.insert_one(data)
            if insert_result is None:
                print("Error while registering")
                return jsonify({"message": "error while registering"}), 404
            else:
                # THIS IS THE CODE TO RUN ON REGISTER
                print("User is registered")
                return jsonify({"message": "User is registered"}), 202
        else:
            print("User is already registered")
            return jsonify({"message": "user is already registered"}), 404
    if request.method == "OPTIONS":
        # Handle the OPTIONS request
        response = app.make_response('')
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        return response

if __name__ == '__main__':
    app.run(debug=True, port=5001)
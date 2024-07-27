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


@app.route('/setProfileData', methods=['POST','GET', 'OPTIONS'])
def set_data():
    if request.method == "POST":
        data = request.get_json()
        description = data.get('description')
        details = data.get('details')
        detailsArr = details.split()
        username = detailsArr[0]
        password = detailsArr[1]
        result = collection.find_one({'username': username})
        # Result being none should really never happen since you already signed in but its good to check
        if result is None:
            return jsonify({"message": "User could not be found"}), 404
        else:
            document_id = result['_id']
            addDesc = {
                '$set': {
                    'description': description
                }
            }
            collection.update_one({'_id': document_id}, addDesc)
            return jsonify({"message": "Data successfully set"}), 202
    if request.method == "OPTIONS":
        # Handle the OPTIONS request
        response = app.make_response('')
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        return response

if __name__ == '__main__':
    app.run(debug=True, port=5003)
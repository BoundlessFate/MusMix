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

# store favorite songs in user data
@app.route('/search', methods=['POST','GET','OPTIONS'])
def update_info():
    print(1111)
    # get cookie
    cookie_val = request.cookies.get('login')
    if request.method == "POST":
        print(2222222)
        #cookie exist only when user logged in
        if cookie_val is not None:
            splitted_val = cookie_val.split(" ")
            username = splitted_val[0].strip()
            password = splitted_val[1].strip()
            auth = sha256.generate_hash(username + password).hex()
            data = request.get_json()
            '''
            not sure if we can save multiple sounds at the same time
            this can reduce the frequency we call update_one()
            '''
            songNames = data.get('soundName',[])  

            result = collection.update_one(
                {'auth': auth},
                {'$addToSet': {'favorite_songs': {'$each': songNames}}}
            )
            if result.matched_count == 0:
                print("Didn't find user")
                return jsonify({"message": "Didn't find user"}), 404
            elif result.modified_count == 0:
                print("Update failed")
                return jsonify({"message": "Update failed"}), 404
            else:
                print("Update success")
                return jsonify({"message": "Login success"}), 200
        
    if request.method == "OPTIONS":
        # Handle the OPTIONS request
        response = app.make_response('')
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        return response

if __name__ == '__main__':
    app.run(debug=True, port=5000)

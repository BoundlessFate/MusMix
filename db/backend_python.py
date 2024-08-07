# Due to port restrictions, these all run off the same app (so the same port could be used)
# They use separate routing though so it should all be fine anyway.

from flask import Flask, request, jsonify
from flask_cors import CORS
import pymongo
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from sha import sha256
import dbConnection
import os

app = Flask(__name__)
CORS(app)

client = None
collection = None
db = None
with app.app_context():
    db = dbConnection.connect_mongo()
    collection = db['userdata']

# uploadPhoto
@app.route('/uploadPhoto', methods=['POST','GET', 'OPTIONS'])
def upload_photo():
    if request.method == "POST":
        UPLOAD_FOLDER = os.path.join(os.getcwd(), 'photos')
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        if 'file' not in request.files:
            return jsonify({"message": "no file sent to flask"}), 404
        else:
            file = request.files['file']
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            details = request.get_json().get('details')
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
                        'photo': file.filename
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


# getProfileData
@app.route('/getProfileData', methods=['POST','GET', 'OPTIONS'])
def get_data():
    if request.method == "POST":
        data = request.get_json()
        details = data.get('details')
        detailsArr = details.split()
        username = detailsArr[0]
        password = detailsArr[1]
        result = collection.find_one({'username': username})
        # Result being none should really never happen since you already signed in but its good to check
        if result is None:
            return jsonify({"message": "User could not be found"}), 404
        else:
            if "description" in result.keys():
                allSongs = songsOne
                allSongs['tracks']['items'] = allSongs['tracks']['items'] + songsTwo['tracks']['items']
                allSongs['tracks']['items'] = allSongs['tracks']['items'] + songsThree['tracks']['items']
                allSongs['tracks']['items'] = allSongs['tracks']['items'] + songsFour['tracks']['items']
            else:
                # Gather 100 songs in the same genre
                # Makes a total of 2 calls to search endpoint, 1 to features per genre
                songsOne = sp.search(q=f"genre:{genre}", type="track", limit=50, offset=0)
                songsTwo = sp.search(q=f"genre:{genre}", type="track", limit=50, offset=1)
                allSongs = songsOne
                allSongs['tracks']['items'] = allSongs['tracks']['items'] + songsTwo['tracks']['items']
            songIds = []
            featuresFull = []
            i = 0
            for song in allSongs['tracks']['items']:
                if i >= 100:
                    featuresFull = featuresFull + sp.audio_features(songIds)
                    songIds = []
                    i = 0
                songIds.append(song['id'])
                i += 1
            if len(songIds) > 0:
                featuresFull = featuresFull + sp.audio_features(songIds)
            for song, songFeatures in zip(allSongs['tracks']['items'], featuresFull):
                # print("song:",song)
                if song['name']+" "+song['artists'][0]['name'] in checkedSongs:
                    continue
                else:
                    checkedSongs.add(song['name']+" "+song['artists'][0]['name'])
                # Skip if song is what was searched
                if song['id'] == track['id']:
                    continue
                if songFeatures['key'] != features['key']:
                    continue
                if songFeatures['mode'] != features['mode']:
                    continue
                val = (song['popularity']) * 3
                val -= abs(songFeatures['tempo']-features['tempo'])
                val -= abs(songFeatures['energy']-features['energy']) * 100
                val -= abs(songFeatures['danceability']-features['danceability']) * 100
                val -= abs(songFeatures['valence']-features['valence']) * 100
                songVals.append((
                    val,
                    f'''
                    <img src="{song["album"]["images"][0]["url"]}">
                    # <h3>{song["name"]} <i>{song["artists"][0]["name"]}</i></h3>
                    '''
                ))

        songVals.sort(key=lambda tup: tup[0], reverse = True)
        i = 1
        finalMessage = [""]*10
        for song in songVals:
            if (i > 10):
                break
            print("-----")
            print("#"+str(i))
            print(f"Track Name & Artist: {song[1]}")
            print(f"Score: {int(song[0])}")
            finalMessage[i - 1] = song[1] + "\n"

            
            i += 1
        if len(songVals)!=0:
            # THIS IS THE CODE TO RUN WHEN SONGS FOUND
            print("Songs are found")
            response = {
                #set each final message to an index in finalMessage
                "m1": finalMessage[0],
                "m2": finalMessage[1],
                "m3": finalMessage[2],
                "m4": finalMessage[3],
                "m5": finalMessage[4],
                "m6": finalMessage[5],
                "m7": finalMessage[6],
                "m8": finalMessage[7],
                "m9": finalMessage[8],
                "m10": finalMessage[9],
                "artist": track['artists'][0]['name'],
                "song": track['name'],
                "album": track['album']['artists'][0]['href']
            }
            
            return jsonify(response), 202
        else:
            # 0 songs are returned
            print("User is already registered")
            return jsonify({"message": "We searched everywhere under the sun, and no songs could be found!"}), 404
    if request.method == "OPTIONS":
        # Handle the OPTIONS request
        response = app.make_response('')
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        return response
# setProfileData
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
    app.run(debug=True, host='0.0.0.0', ssl_context='adhoc')
# Due to port restrictions, these all run off the same app (so the same port could be used)
# They use separate routing though so it should all be fine anyway.

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pymongo
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from sha import sha256
import dbConnection
import os
import random

app = Flask(__name__)
CORS(app)
# Folder for the photos to be MusMix/uploads
UPLOAD_FOLDER = '/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

client = None
collection = None
db = None
with app.app_context():
    db = dbConnection.connect_mongo()
    collection = db['userdata']

@app.route('/uploads/<filename>')
def download_file(filename):
    print(os.listdir(app.config['UPLOAD_FOLDER']))
    print(app.config['UPLOAD_FOLDER'])
    print(filename)
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename, as_attachment=True)

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
            response = {}
            if "description" in result.keys():
                response["description"] = result["description"]
                print(result["description"])
            if "photo" in result.keys():
                response["photo"] = result["photo"]
            if "favorite_songs" in result.keys():
                response["favorite_songs"] = result["favorite_songs"]
            if "favorite_genres" in result.keys():
                response["favorite_genres"] = result["favorite_genres"]
            return jsonify(response), 202

    if request.method == "OPTIONS":
        # Handle the OPTIONS request
        response = app.make_response('')
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        return response

# Register
@app.route('/register', methods=['POST','GET', 'OPTIONS'])
def user_register():
    if request.method == "POST":
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        auth = sha256.generate_hash(username + password).hex()
        data = {
            'username': username,
            'auth': auth
        }
        result = collection.find_one({'username': username})
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
            print("Username is already in use")
            return jsonify({"message": "Username is already in use"}), 404
    if request.method == "OPTIONS":
        # Handle the OPTIONS request
        response = app.make_response('')
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        return response
# Login
@app.route('/login', methods=['POST','GET','OPTIONS'])
def user_login():
    if request.method == "POST":
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        auth = sha256.generate_hash(username + password).hex()
        result = collection.find_one({'username': username})
        if result is None:
            print("Incorrect username or password")
            return jsonify({"message": "Incorrect username or password"}), 404
        else:
            if result["auth"] == auth:
                print("Login success")
                return jsonify({"message": "Login success"}), 200
            else:
                print("Incorrect username or password")
                return jsonify({"message": "Incorrect username or password"}), 404
    if request.method == "OPTIONS":
        # Handle the OPTIONS request
        response = app.make_response('')
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        return response
    
# Search Normal
@app.route('/search', methods=['POST','GET', 'OPTIONS'])
def user_search():
    if request.method == "POST":
        data = request.get_json()
        songName = data.get('name')
        artist = data.get('artist')
        print(songName)
        print(artist)
        clientId = "89ed1b35def340909aa9b514ed93291e"
        clientSecret = "1f50f138da1d42cd8adeedbbe904d8cd"
        authManager = SpotifyClientCredentials(client_id=clientId, client_secret=clientSecret)
        sp = spotipy.Spotify(auth_manager=authManager)

        results = sp.search(q=f"track:{songName} artist:{artist}", type='track')
        track = results['tracks']['items'][0]
        genres = sp.artist(sp.search(q=track['artists'][0]['name'], type='artist', limit=1)['artists']['items'][0]['id'])['genres']
        features = sp.audio_features(track['id'])[0]
        # Extract the first track (assuming it's the most relevant match)

        # Print some basic information about the track
        print(f"Track Name: {track['name']}")
        print(f"Album: {track['album']['artists'][0]['href']}")
        print(f"Artist: {track['artists'][0]['name']}")
        print(f"Image: {track['album']['images'][0]['height']}")
        print(f"Genres: {genres}")
        print("-----FEATURES-----")
        print(f"BPM: {features['tempo']}")
        print(f"Key: {features['key']}")
        print(f"Mode: {features['mode']}")
        print(f"Acousticness: {features['acousticness']}")
        print(f"Danceability: {features['danceability']}")
        print(f"Energy: {features['energy']}")
        print(f"Speechiness: {features['speechiness']}")
        print(f"Valence: {features['valence']}")
        print("-----NOW SEARCHING FOR OTHER SONGS-----")

        # IF THE USER IS LOGGED IN, SAVE THIS SONG FOR THEM AS A "FAVORITED SONG"... ALSO SAVE ALL THE GENRES!
        #cookie exist only when user logged in
        details = data.get('details')
        if details is not None:
            detailsArr = details.split()
            username = detailsArr[0]
            password = detailsArr[1]
            auth = sha256.generate_hash(username + password).hex()
            result = collection.find_one({'auth': auth})
            #update to MongoDB
            # If song has previously been added
            favSongsNew = []
            if "favorite_songs" in result.keys():
                favSongsNew = result["favorite_songs"]
            # Add the new song
            newSongName = track['name']
            # Get rid of any duplicates
            if newSongName not in favSongsNew:
                favSongsNew.append(track['name'])
            
            # Keep only the last 5 entries
            favSongsNew = favSongsNew[-5:]
            document_id = result['_id']
            addFavSongs = {
                '$set': {
                    'favorite_songs': favSongsNew
                }
            }
            collection.update_one({'_id': document_id}, addFavSongs)

            # Do the same as adding songs but add the genres
            favGenresNew = []
            if "favorite_genres" in result.keys():
                favGenresNew = result["favorite_genres"]
            # Add the new genres
            for g in genres:
                favGenresNew.append(g)
            # Get rid of any duplicates
            favGenresNew = list(set(favGenresNew))
            # Keep only the last 5 entries
            favGenresNew = favGenresNew[-5:]
            document_id = result['_id']
            addFavGenres = {
                '$set': {
                    'favorite_genres': favGenresNew
                }
            }
            collection.update_one({'_id': document_id}, addFavGenres)

        checkedSongs=set()
        songVals = []
        for genre in genres:
            allSongs = []
            if (len(genres) <= 2):
                # Gather 200 songs in the same genre
                # Makes a total of 4 calls to search endpoint, 2 to features per genre
                songsOne = sp.search(q=f"genre:{genre}", type="track", limit=50, offset=0)
                songsTwo = sp.search(q=f"genre:{genre}", type="track", limit=50, offset=1)
                songsThree = sp.search(q=f"genre:{genre}", type="track", limit=50, offset=2)
                songsFour = sp.search(q=f"genre:{genre}", type="track", limit=50, offset=3)
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
    
# Search Genres
@app.route('/recommended', methods=['POST','GET', 'OPTIONS'])
def user_recommended():
    if request.method == "POST":
        data = request.get_json()
        details = data.get('details')
        detailsArr = details.split()
        username = detailsArr[0]
        password = detailsArr[1]
        auth = sha256.generate_hash(username + password).hex()
        result = collection.find_one({'auth': auth})
        genres = []
        if "favorite_genres" in result.keys():
            genres = result["favorite_genres"]
        else:
            return jsonify({"message": "We searched everywhere under the sun, and no songs could be found!"}), 404
        clientId = "89ed1b35def340909aa9b514ed93291e"
        clientSecret = "1f50f138da1d42cd8adeedbbe904d8cd"
        authManager = SpotifyClientCredentials(client_id=clientId, client_secret=clientSecret)
        sp = spotipy.Spotify(auth_manager=authManager)

        print(f"Genres: {genres}")

        checkedSongs=set()
        songVals = []
        for genre in genres:
            allSongs = []
            if (len(genres) <= 2):
                # Gather 200 songs in the same genre
                # Makes a total of 4 calls to search endpoint, 2 to features per genre
                songsOne = sp.search(q=f"genre:{genre}", type="track", limit=50, offset=0)
                songsTwo = sp.search(q=f"genre:{genre}", type="track", limit=50, offset=1)
                songsThree = sp.search(q=f"genre:{genre}", type="track", limit=50, offset=2)
                songsFour = sp.search(q=f"genre:{genre}", type="track", limit=50, offset=3)
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
                # Skew random value towards more popular songs, but have enough randomness that new songs pop up
                val = (song['popularity']) + random.randint(0, 100)
                songVals.append((
                    val,
                    f'''
                    <img src="{song["album"]["images"][0]["url"]}" style="width: 10%; height: auto;">
                    <h3>{song["name"]}</h3>
                    <h3><i>{song["artists"][0]["name"]}</i></h3>
                    '''
                ))
                # songVals.append((str(val)+"<strong> "+ song['name']+"</strong> <i>"+song['artists'][0]['name']+"</i>"))
        songVals.sort(key=lambda tup: tup[0], reverse = True)
        i = 1
        finalMessage1 = ""
        finalMessage2 = ""
        finalMessage3 = ""
        finalMessage4 = ""
        finalMessage5 = ""
        finalMessage6 = ""
        finalMessage7 = ""
        finalMessage8 = ""
        finalMessage9 = ""
        finalMessage10 = ""

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
                "m1": finalMessage1,
                "m2": finalMessage2,
                "m3": finalMessage3,
                "m4": finalMessage4,
                "m5": finalMessage5,
                "m6": finalMessage6,
                "m7": finalMessage7,
                "m8": finalMessage8,
                "m9": finalMessage9,
                "m10": finalMessage10
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
# uploadPhoto
@app.route('/uploadPhoto', methods=['POST','GET', 'OPTIONS'])
def upload_photo():
    if request.method == "POST":
        details = request.form['details']
        file = request.files['file']
        detailsArr = details.split()
        username = detailsArr[0]
        password = detailsArr[1]
        result = collection.find_one({'username': username})
        # Result being none should really never happen since you already signed in but its good to check
        if result is None:
            return jsonify({"message": "User could not be found"}), 404
        else:
            # Save the file under /uploads in the server
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            document_id = result['_id']
            addPhoto = {
                '$set': {
                    'photo': filename
                }
            }
            collection.update_one({'_id': document_id}, addPhoto)
            return jsonify({"message": "Data successfully set"}), 202
    if request.method == "OPTIONS":
        # Handle the OPTIONS request
        response = app.make_response('')
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        return response
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)
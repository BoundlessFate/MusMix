from flask import Flask, request, jsonify
from flask_cors import CORS
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

app = Flask(__name__)
CORS(app)

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
            if i==1:
                finalMessage1 = song[1] +"\n"
            elif i==2:
                finalMessage2 = song[1] +"\n"
            elif i==3:
                finalMessage3 =  song[1] +"\n"
            elif i==4:
                finalMessage4 = song[1] +"\n"
            elif i==5:
                finalMessage5 = song[1] +"\n"
            elif i==6:
                finalMessage6 = song[1] +"\n"
            elif i==7:
                finalMessage7 = song[1] +"\n"
            elif i==8:
                finalMessage8 = song[1] +"\n"
            elif i==9:
                finalMessage9 = song[1] +"\n"
            elif i==10:
                finalMessage10 =  song[1] +"\n"

            
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
                "m10": finalMessage10,
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

if __name__ == '__main__':
    app.run(debug=True, port=5002)
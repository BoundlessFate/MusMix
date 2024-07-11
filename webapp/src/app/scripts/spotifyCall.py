import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
n = len(sys.argv)
assert n == 3 # If this fails then the wrong number of args is used
songName = sys.argv[1].replace("_"," ")
artist=sys.argv[2].replace("_"," ")

clientId = "89ed1b35def340909aa9b514ed93291e"
clientSecret = "1f50f138da1d42cd8adeedbbe904d8cd"
authManager = SpotifyClientCredentials(client_id=clientId, client_secret=clientSecret)
sp = spotipy.Spotify(auth_manager=authManager)

results = sp.search(q=f"track:{songName} artist:{artist}", type='track')
track = results['tracks']['items'][0]
genres = sp.artist(sp.search(q=artist, type='artist', limit=1)['artists']['items'][0]['id'])['genres']
features = sp.audio_features(track['id'])[0]
# Extract the first track (assuming it's the most relevant match)

# Print some basic information about the track
print(f"Track Name: {track['name']}")
print(f"Artist: {track['artists'][0]['name']}")
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
        songVals.append((val, song['name']+" "+song['artists'][0]['name']))
songVals.sort(key=lambda tup: tup[0], reverse = True)
i = 1
for song in songVals:
    if (i > 10):
        break
    print("-----")
    print("#"+str(i))
    print(f"Track Name & Artist: {song[1]}")
    print(f"Score: {int(song[0])}")
    i += 1
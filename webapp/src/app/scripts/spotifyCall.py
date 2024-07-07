import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
n = len(sys.argv)
assert n == 3 # If this fails then the wrong number of args is used
songName = sys.argv[1].replace("_"," ")
artist=sys.argv[2].replace("_"," ")

clientId = "d9afeae6b5b74514854e96dd6ad73883"
clientSecret = "7f6556afb86445bfb1d2f7b6b1b0186c"
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
bpmTolerance=30
for genre in genres:
    # Gather 50 songs in the same genre
    allSongs = sp.search(q=f"genre:{genre}", type="track", limit=50)
    for song in allSongs['tracks']['items']:
            # Song is good if it hit this point
    #    print(f"Track Name: {song['name']}")
    #   print(f"Artist: {song['artists'][0]['name']}")
        # Skip if song is what was searched
        if song['id'] == track['id']:
            continue
        curFeatures = sp.audio_features(song['id'])[0]
        if curFeatures['key'] != features['key']:
            continue
        if curFeatures['mode'] != features['mode']:
            continue
        if curFeatures['tempo'] - bpmTolerance > features['tempo']:
            continue
        if curFeatures['tempo'] + bpmTolerance < features['tempo']:
            continue
        # Song is good if it hit this point
        print(f"Track Name: {song['name']}")
        print(f"Artist: {song['artists'][0]['name']}")
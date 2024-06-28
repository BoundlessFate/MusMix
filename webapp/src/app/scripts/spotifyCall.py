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
# Extract the first track (assuming it's the most relevant match)
track = results['tracks']['items'][0]

# Print some basic information about the track
print(f"Track Name: {track['name']}")
print(f"Artist: {track['artists'][0]['name']}")
print(f"Album: {track['album']['name']}")
print(f"Release Date: {track['album']['release_date']}")
print(f"Popularity: {track['popularity']}")
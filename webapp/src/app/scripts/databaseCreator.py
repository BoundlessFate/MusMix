import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time

fileIn = "allgenres.txt"
fileOut = "songdatabase.json"
songsPerGenre = 500

clientId = "89ed1b35def340909aa9b514ed93291e"
clientSecret = "1f50f138da1d42cd8adeedbbe904d8cd"
authManager = SpotifyClientCredentials(client_id=clientId, client_secret=clientSecret)
sp = spotipy.Spotify(auth_manager=authManager)

def writeSongData(fOut, songs, sp, songsLeft):
    songIds = []
    for song in songs['tracks']['items']:
        songIds.append(song['id'])
    featuresFull = sp.audio_features(songIds)
    i = 0
    for song, features in zip(songs['tracks']['items'], featuresFull):
        fOut.write("\t\t\t\""+song['name'].replace('"', '\\"')+" - "+song['artists'][0]['name'].replace('"', '\\"')+"\": {\n")
        fOut.write("\t\t\t\t\"title\": \""+song['name'].replace('"', '\\"')+"\",\n")
        fOut.write("\t\t\t\t\"artist\": \""+song['artists'][0]['name'].replace('"', '\\"')+"\",\n")
        fOut.write("\t\t\t\t\"release_date\": \""+song['album']['release_date']+"\",\n")
        fOut.write("\t\t\t\t\"popularity\": \""+str(song['popularity'])+"\",\n")
        fOut.write("\t\t\t\t\"bpm\": \""+str(features['tempo'])+"\",\n")
        fOut.write("\t\t\t\t\"key\": \""+str(features['key'])+"\",\n")
        fOut.write("\t\t\t\t\"mode\": \""+str(features['mode'])+"\",\n")
        fOut.write("\t\t\t\t\"acousticness\": \""+str(features['acousticness'])+"\",\n")
        fOut.write("\t\t\t\t\"danceability\": \""+str(features['danceability'])+"\",\n")
        fOut.write("\t\t\t\t\"energy\": \""+str(features['energy'])+"\",\n")
        fOut.write("\t\t\t\t\"speechiness\": \""+str(features['speechiness'])+"\",\n")
        fOut.write("\t\t\t\t\"valence\": \""+str(features['valence'])+"\"\n")
        i += 1
        if i >= songsLeft:
            fOut.write("\t\t\t}\n")
        else:
            fOut.write("\t\t\t},\n")
    return

with open(fileIn, 'r') as fIn:
    with open(fileOut, 'w', encoding="utf-8") as fOut:
        fOut.write("{\n\t\"genres\": {\n")
        # Read each line using a loop
        line = fIn.readline()
        while line != "":
            genre = line.strip()
            print(f"Current Genre: {genre}")
            fOut.write("\t\t\""+genre+"\": {\n")
            page = 0
            songsLeft = songsPerGenre
            # Create a list of songs to skip duplicates, which happens for some reason sometimes
            songList = []
            zeroCount = 0
            while(songsLeft > 0):
                # Sleep for a third of a second
                # Makes it so the code doesn't exceed the rate limit of ~180+ calls per minute
                # Or 1 for every third of a second
                time.sleep(0.333)
                i = 50
                if (songsLeft < 50):
                    i = songsLeft
                keysToRemove = []
                allSongs = dict()
                if (songsLeft > 50):
                    songsOne = sp.search(q=f"genre:{genre}", type="track", limit=i, offset=page)
                    time.sleep(0.333)
                    songsTwo = sp.search(q=f"genre:{genre}", type="track", limit=i, offset=page+1)
                    allSongs = songsOne
                    allSongs['tracks']['items'] = allSongs['tracks']['items'] + songsTwo['tracks']['items']
                    page += 2
                else:
                    allSongs = sp.search(q=f"genre:{genre}", type="track", limit=i, offset=page)
                    page += 1
                for song in allSongs['tracks']['items']:
                    if song['name']+" "+song['artists'][0]['name'] in songList:
                        songsLeft -= 1
                        keysToRemove.append(song)
                        continue
                    else:
                        songList.append(song['name']+" "+song['artists'][0]['name'])
                for key in keysToRemove:
                    allSongs['tracks']['items'].remove(key)
                # Writes the song data for a given song from the current genre
                writeSongData(fOut, allSongs, sp, songsLeft)
                songsLeft -= len(allSongs['tracks']['items'])
                # If the genre has less than the requested number of songs
                if (len(allSongs['tracks']['items']) == 0):
                    zeroCount += 1
                # Since a full page could be duplicates, check 10 times to reduce wrong guesses at empty genres
                if (zeroCount >= 10):
                    print(genre+" had less than the requested # of songs. Fix the JSON here.")
                    break
            line = fIn.readline()
            if (line == ""):
                fOut.write("\t\t}\n")
            else:
                fOut.write("\t\t},\n")
        fOut.write("\t}\n}")
    fOut.close()
fIn.close()
# -*- coding: utf-8 -*-
"""
author = 'Vincy Hu'

"""

#import packages
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import pandas as pd

client_id = # enter your client id
client_secret = #  enter your client secret
username = # enter your username

# create a dataframe to store infomation of my playlists 
my_playlist =  pd.DataFrame(columns=["id", "spotify_id", "list_name"])

# getting playlist info from spotify
client_credentials_manager = SpotifyClientCredentials(client_id = client_id, client_secret = client_secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

playlists = sp.user_playlists(username) # input your spotify account id here

# converting spotify data into dataframe
while playlists:
    for i, playlist in enumerate(playlists['items']): 
        spotifyid = playlist['id'] 
        listname = playlist['name'] 
        my_playlist = my_playlist.append({'id':i+1 , 
                        'spotify_id': spotifyid,
                        'list_name': listname
                        }, ignore_index=True)
        
    if playlists['next']:
        playlists = sp.next(playlists)
    else:
        playlists = None

# dataframe for song
my_song =  pd.DataFrame(columns=["list_id", "song_id","song_name","artist","popularity",'release_date']
                       )

# getting song info from each playlist
for listid in my_playlist["spotify_id"]:
    songs = []
    content = sp.user_playlist_tracks(username, listid, fields=None, limit=100, offset=0, market=None)
    songs += content['items']
    for song in songs:
        my_song = my_song.append({"list_id" : listid,
                                  "song_id":song['track']['id'],
                                  "song_name":song['track']['name'],
                                  "artist":song['track']['artists'][0]['name'],
                                  "popularity": song['track']['popularity'],
                                  "release_date": song['track']['album']['release_date']},ignore_index=True)

# song feature dataframe
my_feature = pd.DataFrame(columns=["song_id","energy", "liveness","tempo","speechiness",
                                "acousticness","instrumentalness","danceability",
                                "duration_ms","loudness","valence",
                                "mode","key"])
# playlist songs' features
for song in my_song['song_id']:
    features = sp.audio_features(tracks = [song])[0]
    my_feature = my_feature.append({"song_id":song,
                                    "energy":features['energy'], 
                                    "liveness":features['liveness'],
                                    "tempo":features['tempo'],
                                    "speechiness":features['speechiness'],
                                    "acousticness":features['acousticness'],
                                    "instrumentalness":features['instrumentalness'],
                                    "danceability":features['danceability'],
                                    "duration_ms":features['duration_ms'],
                                    "loudness":features['loudness'],
                                    "valence":features['valence'],
                                    "mode":features['mode'],
                                    "key":features["key"],
                                 },ignore_index=True)

# merging the song info and song features dataframe
song_feature = pd.merge(my_song,my_feature,how='left',left_on='song_id', right_on='song_id')
list_song_feature = pd.merge(my_playlist,song_feature,how='left',left_on='spotify_id', right_on='list_id')

# exporting to csv file
list_song_feature.to_csv('playlist.csv')
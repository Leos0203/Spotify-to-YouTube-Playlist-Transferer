import os
import pickle
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_id = ""
client_secret = ""
scope = 'playlist-read-private'
redirect_uri = "https://google.com"

def get_playlist(spotipy, playlist_id):
    return spotipy.playlist(playlist_id=playlist_id)

def get_playlist_tracks(spotipy, playlist_id):
    playlist = spotipy.playlist(playlist_id=playlist_id)
    playlist_tracks = playlist['tracks']['items']
    playlist_track_names = list()
    for item in playlist_tracks:
        artist = item['track']['album']['artists'][0]['name']
        name = item['track']['name']
        playlist_track_names.append(f'{artist} - {name}')
    return playlist_track_names
    
# 6kNlBT8a51YoZG7TuiQV0P - test playlist
playlist_ID = input("Please enter a valid Spotify Playlist ID: ")

if (os.path.exists("spotify_client_id.pickle")):
    with open("spotify_client_id.pickle", 'rb') as client_id_file:
        client_id = pickle.load(client_id_file)
else:
    client_id = input("Please enter your client ID: ")
if (os.path.exists("spotify_client_secret.pickle")):
     with open("spotify_client_secret.pickle", 'rb') as client_secret_file:
        client_secret = pickle.load(client_secret_file)
else:
    client_secret = input("Please enter your client secret: ")

oath_obj = spotipy.SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope
)

token_dict = oath_obj.get_cached_token()
token = token_dict['access_token']

sp = spotipy.Spotify(auth=token)
playlist = get_playlist(sp, playlist_ID)
playlist_track_names = get_playlist_tracks(sp, playlist_ID)
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
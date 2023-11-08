def search_video(youtube, video):
    search_request = youtube.search().list(
        part="id, snippet",
        maxResults=1,
        type="video",
        q=video,
    )
    return search_request.execute()

def make_playlist(youtube, name, description):
    playlist_request = youtube.playlists().insert(
        part="snippet",
        body={
            "snippet": {
                "title": name,
                "description": description,
            }
        },
    )
    return playlist_request.execute()

def insert_video_in_playlist(youtube, playlistID, videoID):
    insert_request = youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlistID,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": videoID,
                },
            }
        },
    )
    return insert_request.execute()

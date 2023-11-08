from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import spotipy
import os, pickle
import youtube, spotify

def main():
    # YouTube Log In Process
    credentials = None

    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            print("Loading Credentials...")
            credentials = pickle.load(token)
            print("Credentials Loaded Successfully!")

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            print("Refreshing Access Token")
            credentials.refresh(Request())
        else:
            print("Fetching New Tokens...")
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secrets.json",
                scopes=["https://www.googleapis.com/auth/youtube.force-ssl"],
            )
            flow.run_local_server(
                port=8080, prompt="consent", authorization_prompt_message=""
            )
            print("Tokens Fetched!")
            credentials = flow.credentials
            with open("token.pickle", "wb") as token:
                print("Saving Credentials...")
                pickle.dump(credentials, token)
                print("Credentials Saved!")

    api_key = ""

    if os.path.exists("api_key.pickle"):
        with open("api_key.pickle", "rb") as api_file:
            print("Loading API key...")
            api_key = pickle.load(api_file)
            print("API key loaded!")
    else:
        api_key = input("Please enter your API Key: ")

    yt = build("youtube", "v3", credentials=credentials, developerKey=api_key)

    # Spotify Log In Process
    sp_client_id = ""
    sp_client_secret = ""
    sp_scope = 'playlist-read-private'
    sp_redirect_uri = "https://google.com"
    
    print('Logging into Spotify...')

    if (os.path.exists("spotify_client_id.pickle")):
        with open("spotify_client_id.pickle", 'rb') as client_id_file:
            sp_client_id = pickle.load(client_id_file)
    else:
        sp_client_id = input("Please enter your client ID: ")
    if (os.path.exists("spotify_client_secret.pickle")):
        with open("spotify_client_secret.pickle", 'rb') as client_secret_file:
            sp_client_secret = pickle.load(client_secret_file)
    else:
        sp_client_secret = input("Please enter your client secret: ")

    oath_obj = spotipy.SpotifyOAuth(
        client_id=sp_client_id,
        client_secret=sp_client_secret,
        redirect_uri=sp_redirect_uri,
        scope=sp_scope)

    token_dict = oath_obj.get_cached_token()
    token = token_dict['access_token']
    sp = spotipy.Spotify(auth=token)
    print('Successfully logged into Spotify!')

    # Transitioning Process
    playlist_ID = input("Please enter a valid Spotify Playlist ID: ") # 6kNlBT8a51YoZG7TuiQV0P - test playlist
    playlist = spotify.get_playlist(sp, playlist_ID)
    playlist_track_names = spotify.get_playlist_tracks(sp, playlist_ID)

    # Search all the tracks on YouTube and save the IDs in a list
    videoIDs = list()
    for track in playlist_track_names:
        search_response = youtube.search_video(yt, track)
        for item in search_response["items"]:
            videoIDs.append(item["id"]["videoId"])

    # Make a playlist with the same playlist name and description as the Spotify playlist
    playlist_response = youtube.make_playlist(yt, playlist['name'], playlist['description'])

    for videoID in videoIDs:
        youtube.insert_video_in_playlist(yt, playlist_response['id'], videoID)

if __name__ == "__main__":
    main()
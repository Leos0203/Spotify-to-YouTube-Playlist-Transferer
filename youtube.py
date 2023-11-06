from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os, sys
import pickle
import spotify

def main():
    credentials = None

    if os.path.exists("token.pickle"):
        with open("token.pickle", 'rb') as token:
            print("Loading Credentials...")
            credentials = pickle.load(token)
            print("Credentials Loaded Successfully!")

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            print('Refreshing Access Token')
            credentials.refresh(Request())
        else:
            print('Fetching New Tokens...')
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secrets.json',
                scopes=["https://www.googleapis.com/auth/youtube.force-ssl"],
            )
            flow.run_local_server(
                port=8080, prompt="consent", authorization_prompt_message=""
            )
            print("Tokens Fetched!")
            credentials = flow.credentials
            with open("token.pickle", 'wb') as token:
                print("Saving Credentials...")
                pickle.dump(credentials, token)
                print("Credentials Saved!")

    api_key = ""

    if os.path.exists("api_key.pickle"):
        with open('api_key.pickle', 'rb') as api_file:
            print('Loading API key...')
            api_key = pickle.load(api_file)
            print('API key loaded!')
    else:
        api_key = input("Please enter your API Key: ")
            
    youtube = build('youtube', 'v3', credentials=credentials, developerKey=api_key)

    videoIDs = list()
    
    for track in spotify.playlist_track_names:
        search_request = youtube.search().list(
            part='id, snippet',
            maxResults=1,
            type='video',
            q = track,
        )
        search_response = search_request.execute()
        for item in search_response['items']:
            videoIDs.append(item['id']['videoId'])
    
    playlist_request = youtube.playlists().insert(
        part='snippet',
        body={
            'snippet': {
                'title': spotify.playlist['name'],
                'description' : spotify.playlist['description']
            }
        }
    )
    playlist_response = playlist_request.execute()

    for id in videoIDs:
        youtube.playlistItems().insert(
            part='snippet',
            body={
                'snippet': {
                    'playlistId': playlist_response['id'],
                    'resourceId' : {
                        'kind' : 'youtube#video',
                        'videoId': id,
                    }
                } 
            }
        ).execute()
    

if __name__ == "__main__":
    main()
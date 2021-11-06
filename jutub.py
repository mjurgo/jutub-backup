import sys
import os
import re
from datetime import datetime

from dotenv import load_dotenv
from googleapiclient.discovery import build


playlist_url = sys.argv[1]
playlist_id = re.search(r'[&?]list=([^&]+)', playlist_url).group(1)

if len(sys.argv) > 2:
    api_key = sys.argv[2]
else:
    load_dotenv()
    api_key = os.environ['YOUTUBE_API']

youtube = build('youtube', 'v3', developerKey=api_key)

videos = []

nextPageToken = None
while True:
    playlist_request = youtube.playlistItems().list(
        part='contentDetails',
        playlistId=playlist_id,
        maxResults=50,
        pageToken=nextPageToken
    )

    playlist_response = playlist_request.execute()

    vid_ids = []
    for item in playlist_response['items']:
        vid_ids.append(item['contentDetails']['videoId'])


    videos_request = youtube.videos().list(
        part='snippet',
        id=','.join(vid_ids),
        maxResults=50
    )

    videos_response = videos_request.execute()

    for item in videos_response['items']:
        video_data = f"Title: {item['snippet']['title']}, channel: {item['snippet']['channelTitle']}\n"
        videos.append(video_data)

    nextPageToken = playlist_response.get('nextPageToken')
    
    if not nextPageToken:
        break


print(len(videos))

filename = datetime.now().strftime('%Y%m%d_%H%M%S_playlista') + '.txt'

with open(filename, 'w', encoding='utf-8') as f:
    for vid in videos:
        f.write(vid)

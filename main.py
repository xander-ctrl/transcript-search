import os
import json
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from concurrent import futures

config_file = "config.json" 

def initialize_config():
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            return json.load(f)
    else:
        config = {}
        config["api_key"] = input("Enter your YouTube Data API key: ")
        with open(config_file, "w") as f:
            json.dump(config, f, indent=4)
        return config

def get_channel_videos(youtube, channel_url):
    channel_name = channel_url.split("/@")[1]

    request = youtube.search().list(
        part="snippet",
        q=channel_name,
        maxResults=1,
        type="channel"
    )
    response = request.execute()

    if response['items']:
        channel_id = response['items'][0]['id']['channelId']
        request = youtube.channels().list(
            part="statistics",
            id=channel_id
        )
        response = request.execute()

        if not response['items']:
            print(f"No channel data found for ID: {channel_id}")
            return [] 

        total_videos = int(response['items'][0]['statistics'].get('videoCount', 0)) 

        request = youtube.playlistItems().list(
            part="snippet",
            playlistId=f"UU{channel_id[2:]}",
            maxResults=min(50, total_videos)
        )
        response = request.execute()

        videos = []
        for item in response['items']:
            videos.append({
                'id': item['snippet']['resourceId']['videoId'],
                'title': item['snippet']['title']
            })

        # If there are more videos, fetch the next page using 'nextPageToken'
        while 'nextPageToken' in response and len(videos) < total_videos:
            request = youtube.playlistItems().list(
                part="snippet",
                playlistId=f"UU{channel_id[2:]}",
                maxResults=min(50, total_videos - len(videos)),
                pageToken=response['nextPageToken']
            )
            response = request.execute()

            for item in response['items']:
                videos.append({
                    'id': item['snippet']['resourceId']['videoId'],
                    'title': item['snippet']['title']
                })

        return videos
    else:
        print(f"Channel '{channel_name}' not found.")
        return []

def get_video_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return transcript 
    except Exception as err:
        print(f"Could not retrieve transcript for video {video_id}. Skipping...")
        return None

def process_video(video, keyword):
    transcript_list = get_video_transcript(video['id'])
    if transcript_list:
        for segment in transcript_list:
            if keyword.lower() in segment['text'].lower():
                return {
                    'video_id': video['id'],
                    'title': video['title'],
                    'timestamp': segment['start'] 
                }
    return None

def search_keyword_in_channel(youtube, channel_url, keyword):
    videos = get_channel_videos(youtube, channel_url)
    results = []
    
    with futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_video, video, keyword) for video in videos]
        for future in futures.as_completed(futures):
            result = future.result()
            if result:
                results.append(result)

    return results

if __name__ == "__main__":
    config = initialize_config()
    api_key = config['api_key']
    youtube = build('youtube', 'v3', developerKey=api_key)

    channel_url = input("Enter YouTube channel URL: ")
    keyword = input("Enter keyword to search: ")

    results = search_keyword_in_channel(youtube, channel_url, keyword)

    if results:
        print("\nSearch Results:")
        results.sort(key=lambda x: x['title']) 
        for result in results:
            print(f"- {result['title']} (https://www.youtube.com/watch?v={result['video_id']}&t={int(result['timestamp'])})")
    else:
        print("No results found.")
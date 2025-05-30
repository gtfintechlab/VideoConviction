import os
from googleapiclient.discovery import build
from utils import save_video_ids_to_file, save_to_json_file, parse_duration

def get_channel_videos(api_key, channel_id):
    """Retrieve all video IDs from a YouTube channel's uploads playlist."""
    youtube = build('youtube', 'v3', developerKey=api_key)

    # Retrieve the uploads playlist ID
    request = youtube.channels().list(
        part='contentDetails',
        id=channel_id
    )
    response = request.execute()

    uploads_playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    # Retrieve all video IDs from the uploads playlist
    video_ids = []
    next_page_token = None

    while True:
        playlist_request = youtube.playlistItems().list(
            part='contentDetails',
            playlistId=uploads_playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        playlist_response = playlist_request.execute()

        for item in playlist_response['items']:
            video_ids.append(item['contentDetails']['videoId'])

        next_page_token = playlist_response.get('nextPageToken')
        if not next_page_token:
            break
    return video_ids


def filter_by_video_length(api_key, video_ids):
    """Filter out videos from the list based on duration."""
    youtube = build('youtube', 'v3', developerKey=api_key)
    shorts_ids = []

    for i in range(0, len(video_ids), 50):
        request = youtube.videos().list(
            part='contentDetails',
            id=','.join(video_ids[i:i + 50])
        )
        response = request.execute()

        for item in response['items']:
            duration = item['contentDetails']['duration']
            # Parse duration in ISO 8601 format (e.g., PT1M, PT45S)
            seconds = parse_duration(duration)
            # Check if the duration is less than 60 seconds
            if seconds != 0 and seconds <= 720:
                shorts_ids.append(item['id'])
    return shorts_ids


def get_channel_metadata(api_key, channel_id):
    """Retrieve metadata for a YouTube channel."""
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.channels().list(
        part='snippet,statistics',
        id=channel_id
    )
    response = request.execute()
    metadata = response['items'][0]
    return metadata


def save_channel_data(api_key, channel_id):
    """Fetch and save video IDs and metadata for a YouTube channel."""
    video_ids = get_channel_videos(api_key, channel_id)
    shorts_ids = filter_by_video_length(api_key, video_ids)
    metadata = get_channel_metadata(api_key, channel_id)

    # # Create a folder with the channel ID
    base_folder = 'channels'
    folder_name = os.path.join(base_folder, channel_id)
    os.makedirs(folder_name, exist_ok=True)

    # # Save video IDs to a .txt file
    videos_filename = os.path.join(folder_name, 'videos.txt')
    save_video_ids_to_file(shorts_ids, videos_filename)

    # # Save metadata to a JSON file
    metadata_filename = os.path.join(folder_name, 'metadata.json')
    save_to_json_file(metadata, metadata_filename)

    print(f"Total Videos: {len(shorts_ids)}")
    print(f"Video IDs saved to {videos_filename}")
    print(f"Metadata saved to {metadata_filename}")

    return shorts_ids, metadata

import os
from googleapiclient.discovery import build
from utils import write_to_csv, transform_to_video_metadata_csv_rows, transform_to_channel_metadata_csv_rows, save_video_ids_to_file, read_channel_ids_from_file
from youtube_data.fetch_channel_videos import save_channel_data
import logging

########## Fetch comments for videos ##########
def get_video_comments(args, video_id, max_comments=50):
    try:
        youtube = build('youtube', 'v3', developerKey=args.api_key)
        comments = []
        next_page_token = None
        request = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            maxResults=100,
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textOriginal']
            comments.append(comment)
            if len(comments) >= max_comments:
                return comments
        return comments
    except Exception as e:
        logging.error(f"Error fetching comments for video {video_id}: {str(e)}")
        return []  # Return empty list in case of error

def save_multiple_channels_data(args, channel_ids):
    all_video_ids = []
    all_channel_metadata = []
    for channel_id in channel_ids:
        shorts_ids, metadata = save_channel_data(args.api_key, channel_id)
        all_video_ids.extend(shorts_ids)
        all_channel_metadata.append(metadata)

    metadata_filename = os.path.join(args.channels_metadata_file)
    columns = ["channelId", "channelDescription", "channelViewCount", "channelSubscriberCount", "videoCount"]
    refined_metadata = transform_to_channel_metadata_csv_rows(all_channel_metadata)

    write_to_csv(metadata_filename, columns, refined_metadata)

    save_video_ids_to_file(all_video_ids, args.video_id_list)
    print(f"All video IDs merged into {args.video_id_list}")


def fetch_metadata_for_videos(args):
    with open(args.video_id_list) as f:
        video_ids = f.read().splitlines()

    metadata_for_videos = []

    for i in range(0, len(video_ids), 50):
        youtube = build('youtube', 'v3', developerKey=args.api_key)
        request = youtube.videos().list(
            part='snippet,statistics,contentDetails,status',
            id=','.join(video_ids[i:i + 50])
        )
        response = request.execute()
        metadata_for_videos.extend(response['items'])

    metadata_filename = os.path.join(args.videos_metadata_file)
    columns = [
        "videoId", "videoTitle", "licenseType", "channelId", "channelTitle", "publishedAt", "videoDescription",
        "tags", "defaultAudioLanguage", "duration", "isCaptionAvailable",
        "viewCount", "likeCount", "favoriteCount", "commentCount"
    ]
    refined_metadata = transform_to_video_metadata_csv_rows(metadata_for_videos)

    write_to_csv(metadata_filename, columns, refined_metadata)


def fetch_comments_for_videos(args):
    with open(args.video_id_list) as f:
        video_ids = f.read().splitlines()
    
    comments_for_videos = []
    
    for video_id in video_ids:
        video_comments = get_video_comments(args, video_id)
        comments_for_videos.append([video_id, video_comments])

    comments_filename = os.path.join(args.videos_comments_file)
    columns = ["videoId", "comments"]
    write_to_csv(comments_filename, columns, comments_for_videos)


def get_youtube_data(args):
    if not os.path.exists(args.dataset_dir):
        os.makedirs(args.dataset_dir, exist_ok=True)

    if not os.path.exists(args.video_id_list):
        # Read channel ids from channel_ids_file
        channel_ids = read_channel_ids_from_file(args.channel_ids)
        save_multiple_channels_data(args, channel_ids)

    if not os.path.exists(args.videos_metadata_file):
        # Generate metadata for videos
        print('Fetch metadata for videos...')
        fetch_metadata_for_videos(args)

    if not os.path.exists(args.videos_comments_file):
        # Get comments for videos
        print('Fetch comments for videos...')
        fetch_comments_for_videos(args)
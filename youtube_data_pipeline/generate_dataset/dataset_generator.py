import os
import pandas as pd


def generate(args):
    # Read CSV files into DataFrames
    try:
        videos_metadata = pd.read_csv(os.path.join(args.videos_metadata_file))
        videos_comments = pd.read_csv(os.path.join(args.videos_comments_file))
        videos_transcripts = pd.read_csv(os.path.join(args.video_transcriptions_file))
        channel_metadata = pd.read_csv(os.path.join(args.channels_metadata_file))
    except Exception as e:
        print(f"Error reading CSV files: {e}")
        return

    # Ensure required columns are present
    required_columns_videos = ['videoId', 'channelId']
    required_columns_comments = ['videoId']
    required_columns_transcripts = ['videoId']
    required_columns_channels = ['channelId']

    for col in required_columns_videos:
        if col not in videos_metadata.columns:
            print(f"Column {col} missing from videos_metadata")
            return

    for col in required_columns_comments:
        if col not in videos_comments.columns:
            print(f"Column {col} missing from videos_comments")
            return

    for col in required_columns_transcripts:
        if col not in videos_transcripts.columns:
            print(f"Column {col} missing from videos_transcripts")
            return

    for col in required_columns_channels:
        if col not in channel_metadata.columns:
            print(f"Column {col} missing from channel_metadata")
            return

    # Merge DataFrames
    comments_and_metadata = pd.merge(videos_metadata, videos_comments, on='videoId', how='inner')
    comments_metadata_and_transcripts = pd.merge(comments_and_metadata, videos_transcripts, on='videoId', how='inner')
    all_video_data = pd.merge(comments_metadata_and_transcripts, channel_metadata, on='channelId', how='inner')

    # Save final dataset to CSV
    dataset_filename = os.path.join(args.preliminary_dataset_file)
    try:
        all_video_data.to_csv(dataset_filename, index=False)
        print(f"Final dataset saved to {dataset_filename}")
    except Exception as e:
        print(f"Error writing final dataset to CSV: {e}")

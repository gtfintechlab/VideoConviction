import argparse
import os
import logging
from dotenv import load_dotenv
from youtube_data.youtube_data_pipeline import get_youtube_data
from filter_and_sample.video_filter import filter_videos
from filter_and_sample.sampling import create_video_sample
from youtube_data.video_downloader import download_videos
from transcripts.transcript_generator import generate_transcripts
from generate_dataset.dataset_generator import generate

load_dotenv('.env')
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')


def pipeline(args):
    try:
        logging.info("Fetching YouTube data - video, channel metadataand comments...")
        get_youtube_data(args)
    except Exception as e:
        logging.error(f"Error fetching YouTube data: {e}")
        return

    try:
        logging.info("Filtering videos for stock recommendations...")
        filter_videos(args)
    except Exception as e:
        logging.error(f"Error filtering videos: {e}")
        return

    try:
        logging.info("Creating video sample...")
        create_video_sample(args)
    except Exception as e:
        logging.error(f"Error creating video sample: {e}")
        return

    try:
        logging.info("Downloading sampled videos...")
        download_videos(args)
    except Exception as e:
        logging.error(f"Error downloading videos: {e}")
        return

    try:
        logging.info("Generating transcripts for sample...")
        generate_transcripts(args)
    except Exception as e:
        logging.error(f"Error generating transcripts: {e}")
        return

    try:
        logging.info("Generating final dataset...")
        generate(args)
    except Exception as e:
        logging.error(f"Error generating final dataset: {e}")
        return

    logging.info("Pipeline executed successfully.")


def get_args():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_dir = os.path.join(base_dir, 'dataset')
    channels_dir = os.path.join(base_dir, 'channels')
    video_dir = os.path.join(base_dir, 'videos')
    audio_dir = os.path.join(base_dir, 'audios')

    parser = argparse.ArgumentParser()
    parser.add_argument('--video_dir', type=str, help='Folder to store youtube videos', default=video_dir)

    parser.add_argument('--audio_dir', type=str, help='Folder to store transcript of youtube videos', default=audio_dir)

    parser.add_argument('--num_workers', help='The number of threads', type=int, default=6)

    parser.add_argument('--dataset_dir', type=str, help='Directory where our dataset will be stored',
                        default=dataset_dir)

    parser.add_argument('--video_id_list', type=str, help='Text files with video ids',
                        default=os.path.join(dataset_dir, 'video_ids.text'))

    parser.add_argument('--videos_metadata_file', type=str, help='CSV file with metadata of each video',
                        default=os.path.join(dataset_dir, 'videos_metadata.csv'))

    parser.add_argument('--videos_comments_file', type=str, help='CSV file for comments of each video',
                        default=os.path.join(dataset_dir, 'videos_comments.csv'))

    parser.add_argument('--video_transcriptions_file', type=str, help='CSV file for transcriptions of each video',
                        default=os.path.join(dataset_dir, 'video_transcriptions.csv'))

    parser.add_argument('--channels_metadata_file', type=str, help='CSV file for metadata of each channel',
                        default=os.path.join(dataset_dir, 'channels_metadata.csv'))

    parser.add_argument('--transcript_dir', type=str,
                        help='Folder to store transcripts',
                        default=os.path.join(dataset_dir, 'transcript_files'))

    parser.add_argument('--preliminary_dataset_file', type=str,
                        help='File to store the complete dataset with video metadata, '
                             'channel metadata, comments and transcripts',
                        default=os.path.join(dataset_dir, 'preliminary_dataset.csv'))

    parser.add_argument('--filtered_dataset_file', type=str,
                        help='File to store the filtered dataset containing videos with explicit stock recommendations',
                        default=os.path.join(dataset_dir, 'filtered_dataset.csv'))

    parser.add_argument('--sampled_dataset_file', type=str,
                        help='File to store the sample dataset',
                        default=os.path.join(dataset_dir, 'sampled_dataset.csv'))

    parser.add_argument('--total_videos_to_sample', type=int,
                        default=10)

    parser.add_argument('--past_years_to_consider', type=int,
                        default=3)

    parser.add_argument('--channel_ids', type=str, help='Channel ids for fetching all input channels',
                        default=os.path.join(channels_dir, 'channel_ids.txt'))

    parser.add_argument('--api_key', type=str, help='Youtube API key',
                        default=YOUTUBE_API_KEY)

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = get_args()
    pipeline(args)
import os
import yt_dlp
import pandas as pd
from multiprocessing import Pool


def download_video(url, output_dir):
    ydl_opts = {
        'quiet' : 'True',
        'noplaylist' : 'True',
        'format' : '136+140/135+140/137+140/136+m4a/135+m4a/137+m4a/mp4+140/18/22/mp4+m4a',
        'outtmpl': os.path.join(output_dir, '%(id)s.mp4')  # Save by videoId
    }

    ydl = yt_dlp.YoutubeDL(ydl_opts)

    try:
        ydl.download([url])
        print(f"Downloaded video: {url}")
    except Exception as error:
        print(f"Error downloading video {url}: {error}")


def download_videos_from_csv(csv_file_path, output_dir, num_workers):
    try:
        df = pd.read_csv(csv_file_path)
        video_ids = df['videoId'].tolist()
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return

    urls = ['https://youtube.com/watch?v=' + video_id for video_id in video_ids]

    print(f"Total URLs to download: {len(urls)}")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    # Download videos in parallel
    with Pool(num_workers) as pool:
        pool.starmap(download_video, [(url, output_dir) for url in urls])


def download_videos(args):
    if not os.path.exists(args.video_dir):
        os.makedirs(args.video_dir, exist_ok=True)

    download_videos_from_csv(args.sampled_dataset_file, args.video_dir, args.num_workers)
import os
import pandas as pd
from glob import glob
from multiprocessing import Pool
from pathlib import Path
import whisper
from utils import write_to_csv


########## Extract Audios ##########
def extract_audio(video_path, audio_dir, video_id):
    audio_path = os.path.join(audio_dir, f"{video_id}.mp3")
    try:
        if not os.path.exists(audio_path):
            os.system(f'ffmpeg -y -i "{video_path}" -b:a 128k "{audio_path}"')
            print(f"Audio saved at {audio_path}.")
        else:
            print(f"Audio already exists at {audio_path}.")
    except Exception as e:
        print('Error with video:', video_path, 'Error:', e)


def extract_audios(args):
    if not os.path.exists(args.audio_dir):
        os.makedirs(args.audio_dir, exist_ok=True)
    video_paths = glob(os.path.join(args.video_dir, '*.mp4'))
    video_ids_from_filenames = [Path(video_path).stem for video_path in video_paths]
    video_paths_dict = {Path(video_path).stem: video_path for video_path in video_paths}
    video_audio_mappings = [(video_paths_dict[video_id], args.audio_dir, video_id) for video_id in
                            video_ids_from_filenames]

    if len(video_paths) == 0:
        print('Warning : Length of video list is 0.')
    with Pool(args.num_workers) as pool:
        pool.starmap(extract_audio, video_audio_mappings)


########## Speech-to-Text ##########
def aggregate_segment_wise_transcripts(args):
    # Load the original sampled dataset file
    original_dataset = pd.read_csv(args.sampled_dataset_file)

    # Load individual transcript files and combine them
    transcript_files = glob(os.path.join(args.transcript_dir, '*.txt'))
    transcriptions = []

    for file_path in transcript_files:
        # Extract videoId, start_time, and end_time from the file name
        file_name = Path(file_path).stem
        video_id, start_time, end_time = file_name.split('__')

        with open(file_path, 'r') as f:
            transcript_text = f.read()

        transcriptions.append({
            'videoId': video_id,
            'start': float(start_time),
            'end': float(end_time),
            'transcript': transcript_text
        })

    # Create a DataFrame for combined transcripts
    transcripts_df = pd.DataFrame(transcriptions)

    # Merge with the original dataset using videoId, start, and end as a composite key
    final_transcriptions = original_dataset.merge(
        transcripts_df,
        on=['videoId', 'start', 'end'],
        how='left'
    )

    # Save to a CSV file
    transcriptions_filename = args.video_transcriptions_file
    final_transcriptions.to_csv(transcriptions_filename, index=False)
    print(f"All transcripts aggregated with full metadata and saved to {transcriptions_filename}.")


def run_whisper_for_segments(args):
    df = pd.read_csv(args.sampled_dataset_file)
    model = whisper.load_model("large-v2")

    # Ensure the transcript directory exists
    if not os.path.exists(args.transcript_dir):
        os.makedirs(args.transcript_dir, exist_ok=True)

    for _, row in df.iterrows():
        video_id = row['videoId']
        start_time = row['start']
        end_time = row['end']

        audio_path = os.path.join(args.audio_dir, f"{video_id}.mp3")
        segment_audio_path = os.path.join(args.audio_dir, f"{video_id}__{start_time}__{end_time}.mp3")
        segment_transcript_path = os.path.join(args.transcript_dir, f"{video_id}__{start_time}__{end_time}.txt")

        if os.path.exists(segment_transcript_path):
            print(f"Transcript for segment {video_id} ({start_time}-{end_time}) already exists. Skipping...")
            continue

        if os.path.exists(audio_path):
            try:
                # Extract audio segment
                os.system(f'ffmpeg -y -i "{audio_path}" -ss {start_time} -to {end_time} -c copy "{segment_audio_path}"')

                # Transcribe the segment
                result = model.transcribe(segment_audio_path)
                transcript_text = result['text']

                # Save segment transcript
                with open(segment_transcript_path, 'w') as f:
                    f.write(transcript_text)
                print(f"Segment transcript saved at {segment_transcript_path}.")
            except Exception as e:
                print(f"Error transcribing segment {video_id} ({start_time}-{end_time}): {e}")
        else:
            print(f"Audio file {audio_path} does not exist. Please extract audio first.")

    # Combine all transcripts into a final CSV
    aggregate_segment_wise_transcripts(args)


def aggregate_transcripts(args):
    transcript_files = glob(os.path.join(args.transcript_dir, '*.txt'))
    transcriptions = []
    for file_path in transcript_files:
        video_id = Path(file_path).stem
        with open(file_path, 'r') as f:
            transcript_text = f.read()
        transcriptions.append([video_id, transcript_text])
    transcriptions_filename = args.video_transcriptions_file
    column_names = ['videoId', 'transcript']
    write_to_csv(transcriptions_filename, column_names, transcriptions)
    print(f"All transcripts aggregated and saved to {transcriptions_filename}.")


def run_whisper(args):
    df = pd.read_csv(args.sampled_dataset_file)
    video_ids = df['videoId'].tolist()
    model = whisper.load_model("large-v2")

    # Ensure the transcript directory exists
    if not os.path.exists(args.transcript_dir):
        os.makedirs(args.transcript_dir, exist_ok=True)

    for video_id in video_ids:
        audio_path = os.path.join(args.audio_dir, f"{video_id}.mp3")
        transcript_path = os.path.join(args.transcript_dir, f"{video_id}.txt")

        if os.path.exists(transcript_path):
            print(f"Transcript for {video_id} already exists. Skipping...")
            continue

        if os.path.exists(audio_path):
            try:
                result = model.transcribe(audio_path)
                transcript_text = result['text']

                # Save each transcript individually
                with open(transcript_path, 'w') as f:
                    f.write(transcript_text)
                print(f"Transcript saved at {transcript_path}.")
            except Exception as e:
                print(f"Error transcribing {audio_path}: {e}")
        else:
            print(f"Audio file {audio_path} does not exist.")

    # Gather all transcripts into a final CSV
    aggregate_transcripts(args)


def generate_transcripts(args):
    # extract audio
    print('Extract audios from videos...')
    extract_audios(args)

    # run whisper
    print('Transcribe audios...')
    if (args.generate_segment_wise_transcripts):
        run_whisper_for_segments(args)
    else:
        run_whisper(args)
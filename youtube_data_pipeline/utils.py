import csv
import json

###### Transformation Functions ######
def transform_to_channel_metadata_csv_rows(metadata_for_channels):
    """
    Transforms channel metadata into rows suitable for a CSV file.

    :param metadata_for_channels: list of metadata objects.
    :return: list of lists, where each sublist represents a row in the CSV file.
    """
    refined_metadata_for_channels = []

    for metadata in metadata_for_channels:
        refined_row = [
            metadata["id"],
            remove_whitespaces(metadata["snippet"].get("description", None)),
            metadata["statistics"].get("viewCount", None),
            metadata["statistics"].get("subscriberCount", None),
            metadata["statistics"].get("videoCount", None)
        ]

        refined_metadata_for_channels.append(refined_row)

    return refined_metadata_for_channels


def transform_to_video_metadata_csv_rows(metadata_for_videos):
    """
    Transforms video metadata into rows suitable for a CSV file.

    :param metadata_for_videos: list of metadata objects.
    :return: list of lists, where each sublist represents a row in the CSV file.
    """
    refined_metadata_for_videos = []

    for metadata in metadata_for_videos:
        refined_row = [
            metadata["id"],
            metadata["snippet"].get("title", None),
            metadata["status"].get("license", None),
            metadata["snippet"].get("channelId", None),
            metadata["snippet"].get("channelTitle", None),
            metadata["snippet"].get("publishedAt", None),
            remove_whitespaces(metadata["snippet"].get("description", "")),
            metadata["snippet"].get("tags", None),
            metadata["snippet"].get("defaultAudioLanguage", None),
            parse_duration(metadata["contentDetails"].get("duration", None)),
            metadata["contentDetails"].get("caption", None),
            metadata["statistics"].get("viewCount", None),
            metadata["statistics"].get("likeCount", None),
            metadata["statistics"].get("favoriteCount", None),
            metadata["statistics"].get("commentCount", None)
        ]

        refined_metadata_for_videos.append(refined_row)

    return refined_metadata_for_videos


def remove_whitespaces(my_string):
    """Removes extra whitespaces from a string."""
    return ' '.join(my_string.split())


def parse_duration(duration):
    """
    Parses ISO 8601 duration format into seconds.

    :param duration: str, ISO 8601 duration format.
    :return: int, duration in seconds.
    """
    if duration == 'P0D':
        return 0
    # Parse the ISO 8601 duration format
    iso_duration = duration[2:]  # Remove 'PT' prefix
    time_dict = {'H': 3600, 'M': 60, 'S': 1}
    seconds = 0
    number = ''

    for char in iso_duration:
        if char.isdigit():
            number += char
        else:
            seconds += int(number) * time_dict[char]
            number = ''
    return seconds

###### Write Functions ######
def save_to_json_file(data, filename):
    """
    Saves data to a JSON file.

    :param data: dict, the data to be saved.
    :param filename: str, the name of the JSON file to be created.
    """
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)


def save_video_ids_to_file(video_ids, filename):
    """
    Saves a list of video IDs to a text file.

    :param video_ids: list of str, the video IDs to be saved.
    :param filename: str, the name of the text file to be created.
    """
    with open(filename, 'w') as file:
        for video_id in video_ids:
            file.write(f"{video_id}\n")


def write_to_csv(filename, column_names, rows):
    """
    Writes data to a CSV file.

    :param filename: str, the name of the CSV file to be created.
    :param column_names: list of str, the column names for the CSV file.
    :param rows: list of lists, where each sublist represents a row in the CSV file.
    """
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if len(column_names):
            writer.writerow(column_names)
        writer.writerows(rows)


###### Read Functions ######
def read_channel_ids_from_file(filename):
    """
    Reads channel IDs from a text file.

    :param filename: str, the name of the text file to be read.
    :return: list of str, the channel IDs read from the file.
    """
    with open(filename, 'r') as file:
        channel_ids = [line.strip() for line in file.readlines()]
    return channel_ids

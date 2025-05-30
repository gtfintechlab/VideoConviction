import pandas as pd


def sample_videos_per_year(data, year, videos_per_year):
    yearly_data = data[data['publishedAt'].dt.year == year]
    yearly_sampled_videos = yearly_data.sample(videos_per_year)

    return yearly_sampled_videos


def categorize_channels(data, total_partitions):
    thresholds = [data['channelViewCount'].quantile(i / total_partitions) for i in range(1, total_partitions)]
    def get_category(view_count):
        for i, threshold in enumerate(thresholds):
            if view_count <= threshold:
                return f'Category {i + 1}'
        return f'Category {total_partitions}'

    data['channelCategory'] = data['channelViewCount'].apply(get_category)

    return data


def sample_videos(data, total_videos, total_years):
    # Determine the current year and the start year
    current_year = data['publishedAt'].dt.year.max()
    start_year = current_year - total_years + 1

    # Filter videos for the last y years
    filtered_data = data[(data['publishedAt'].dt.year >= start_year) & (data['publishedAt'].dt.year <= current_year)]

    # Calculate the number of videos to sample per year
    videos_per_year = total_videos // total_years
    print("videos_per_year", videos_per_year)

    all_sampled_videos = pd.DataFrame()

    for year in range(start_year, current_year + 1):
        sampled_videos_year = sample_videos_per_year(data, year, videos_per_year)
        print("sampled_videos_year", sampled_videos_year.shape[0])
        all_sampled_videos = pd.concat([all_sampled_videos, sampled_videos_year])

    print("all_sampled_videos", all_sampled_videos.shape[0])
    return all_sampled_videos


def create_video_sample(args):
    data = pd.read_csv(args.filtered_dataset_file)
    data['publishedAt'] = pd.to_datetime(data['publishedAt'])

    sampled_videos = sample_videos(data, args.total_videos_to_sample, args.past_years_to_consider)
    sampled_videos.to_csv(args.sampled_dataset_file, index=False)
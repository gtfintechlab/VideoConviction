import pandas as pd
import os
import re

recommendation_keywords = ["buy", "buying", "bought", "sell", "selling", "sold", "hold", "holding", "held", "bullish", "bearish"]
non_recommendation_keyworks = ["analysis", "market analysis", "review", "market review", "crypto", "cryptocurrency", "bitcoin", "btc", "etherium", "eth", "altcoin", "altcoins", "estate"]
security_descriptors = ["best", "top", "worth", "worst", "tanking"]
security_types = ["stock", "stocks", "etf", "etfs", "company", "companies"]


def filter_by_title(title):
    '''
    bool function that takes in a given video title and returns True if it fulfills our criteria

    @ param title: name of the video
    '''

    # approving titles with recommendation verbs
    if check_phrases(title, recommendation_keywords):
        return True

    # approving titles with Best...Stocks format
    if check_regex(title, r'({}).*({})'.format('|'.join(security_descriptors), '|'.join(security_types))):
        return True
    if check_regex(title, r'({}).*({})'.format('|'.join(security_types), '|'.join(security_descriptors))):
        return True

    # eliminating titles with analysis/review
    if check_phrases(title, non_recommendation_keyworks):
        return False
    return False


def check_phrases(sentence, phrases):
    for phrase in phrases:
        if phrase.upper() in sentence.upper().split():
            return True
    return False


def check_regex(sentence, regex):
    multiple_pattern = re.compile(regex.upper())
    if multiple_pattern.search(sentence.upper()):
        return True
    return False


def filter_videos(args):
    preliminary_dataset = pd.read_csv(os.path.join(args.videos_metadata_file))

    title_filter = preliminary_dataset['videoTitle'].apply(lambda title: filter_by_title(title))
    
    filtered_df = preliminary_dataset[title_filter]
    print("Total Videos: ", filtered_df.shape[0])

    filtered_df.to_csv(os.path.join(args.filtered_dataset_file), index=False)
    print(f"Filtered dataset saved to directory {os.path.join(args.filtered_dataset_file)}!")
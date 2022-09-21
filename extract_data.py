
import os
import json
import gzip
import glob
import argparse
import pandas as pd
from joblib import Parallel, delayed
import multiprocessing as mp
from tqdm import tqdm
tqdm.pandas()

# Initialize arg parse for events:
parser = argparse.ArgumentParser(description="START Ukraine-Russia Tweet Scraper")
parser.add_argument("-s", 
                    "--sheet_name", 
                    help="The sheet within the Excel file to pull data.")
parser.add_argument("-e", 
                    "--event_id", 
                    help="Gets tweets for the listed event.")
parser.add_argument("-rs",
                    "--random_sample",
                    help="A float between 0.0 and 1.0 for sample proportion.")
args = parser.parse_args()


def load_data(path: str) -> list:
    with gzip.open(path, "r") as f:
        data = json.loads(f.read().decode("utf-8"))
    return data


def extract_urls(tweet: dict):
    urls = []
    try:
        for url in tweet["entities"]["urls"]:
            urls.append(url["expanded_url"])
    except Exception:
        pass
    if len(urls) == 0:
        return None
    else:
        return urls
    
    
def extract_hashtags(tweet: dict):
    hashtags = []
    try:
        for hashtag in tweet["entities"]["hashtags"]:
            hashtags.append(hashtag["tag"])
    except Exception:
        pass
    
    if len(hashtags) == 0:
        return None
    else:
        return ",".join(hashtags)
    
    
def extract_tweet_references(tweet: dict):
    if "referenced_tweets" in tweet:
        refs = {}
        for ref in tweet["referenced_tweets"]:
            refs[ref["id"]] = ref["type"]
            
        return refs
    else:
        return "original_tweet"
    
    
def extract_mentions(tweet: dict):
    mentions = {}
    try:
        for mention in tweet["entities"]["mentions"]:
            mentions[mention["id"]] = mention["username"]
    except Exception:
        pass
    
    if len(mentions) == 0:
        return None
    else:
        return mentions
    

def extract_media(tweet: dict):
    media = []
    try:
        for med in tweet["attachments"]["media"]:
            media.append({"type": med["type"], 
                          "url": med["url"], 
                          "media_key": med["media_key"]})
    except KeyError:
        pass
    if len(media) == 0:
        return None
    else:
        return media
    
    
def extract_author_info(tweet: dict):
    author = {}
    
    author["id"] = tweet["id"]
    author["username"] = tweet["username"]
    author["description"] = tweet["description"]
    author["verified"] = tweet["verified"]
    
    try:
        author["location"] = tweet["location"]
    except Exception:
        author["location"] = None
    
    author["url"] = tweet["url"]
    author["profile_image_url"] = tweet["profile_image_url"]
    author["created_at"] = tweet["created_at"]
    author["followers_count"] = tweet["public_metrics"]["followers_count"]
    author["following_count"] = tweet["public_metrics"]["following_count"]
    author["tweet_count"] = tweet["public_metrics"]["tweet_count"]
    author["listed_acount"] = tweet["public_metrics"]["listed_count"]
    author["profile_url"] = f"https://twitter.com/{author['username']}"
        
    return author


def extract_tweet_metadata(tweet: dict):
    output = {}
    
    fields = [
        "id",
        "conversation_id",
        "reply_settings",
        "source",
        "author_id",
        "created_at",
        "text",
        "lang",
        "possibly_sensitive",
    ]
    
    output = {k: tweet[k] for k in fields}
    output["tweet_url"] = f"https://twitter.com/{output['author_id']}/status/{output['id']}"
    
    if "attachments" in tweet.keys():
        output["has_media"] = True
    else:
        output["has_media"] = False
    
    #output["tweet_media"] = extract_media(tweet)
    output["author"] = tweet["author"]["username"]
    output["urls"] = extract_urls(tweet)
    output["referenced_tweets"] = extract_tweet_references(tweet)
    output["hashtags"] = extract_hashtags(tweet)
    output["mentions"] = extract_mentions(tweet)
    
    
    author_info = extract_author_info(tweet["author"])
    
    return output, author_info    


def untuple_results_to_df(tweets: list) -> tuple:
    tweet_data = []
    author_data = []
    
    for tweet in tqdm(tweets):
        tweet_data.append(tweet[0])
        author_data.append(tweet[1])
    
    tweet_data = pd.DataFrame(tweet_data)
    tweet_data["date"] = pd.to_datetime(tweet_data.created_at).dt.date
    
    author_data = pd.DataFrame(author_data)
    author_data.drop_duplicates("id", inplace=True)
    author_data.reset_index(inplace=True, drop=True)

    
    return tweet_data, author_data


def preprocess_tweets_df(df: pd.DataFrame) -> pd.DataFrame:
    coding_cols = [
        "id",
        "author_id",
        "author",
        "tweet_url",
        "has_media",
        "date",
        "text"
    ]
    
    df["text"] = df.text.apply(lambda row: row.replace("\n", " ").strip())
    
    df = df[coding_cols]
    
    return df


def sample_data(tweets: pd.DataFrame, authors: pd.DataFrame, prop: float) -> tuple:
    sampled = pd.DataFrame()
    for date in tqdm(sorted(tweets.date.unique())):
        sampled = pd.concat([
            sampled, 
            tweets[tweets.date == date].sample(frac=prop, random_state=42)
            ])
    
    author_filter = set(sampled.author_id.unique())
    authors = authors[authors.id.isin(author_filter)]
    
    authors.reset_index(inplace=True, drop=True)
    sampled.reset_index(inplace=True, drop=True)
    
    return sampled, authors


if __name__ == "__main__":
    files = glob.glob(os.path.join("data", args.sheet_name, args.event_id, "*.json.gz"))

    print("Loading files...")
    raw_data = Parallel(mp.cpu_count())(delayed(load_data)(f) for f in tqdm(files))

    print("Extracting tweet metadata...")
    tweets = Parallel(mp.cpu_count())(delayed(extract_tweet_metadata)(tweet) for tweet in tqdm(raw_data))

    print("Preapring tweet & author dataframes...")
    tweet_data, author_data = untuple_results_to_df(tweets)
    
    sample = float(args.random_sample)
    print(f"Generating a {sample*100}% random sample...")
    tweet_data, author_data = sample_data(tweet_data, author_data, sample)

    print("Saving outputs...")
    outfile = preprocess_tweets_df(tweet_data)
    outfile.to_csv(os.path.join("data", "processed", args.sheet_name, args.event_id + ".csv"), index=False)
    author_data.to_csv(os.path.join("data", "processed", args.sheet_name, args.event_id + "_authors.csv"), index=False)
    
    print("Done!")
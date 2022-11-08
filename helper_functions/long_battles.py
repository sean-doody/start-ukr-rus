import os
import gzip
import json
import time
import datetime as dt
from twarc import Twarc2, expansions

def kharkiv(start: dt.datetime.timestamp, end: dt.datetime.timestamp):
    batches = [
        (start - dt.timedelta(weeks=1), start),
        (dt.datetime(2022, 3, 1), dt.datetime(2022, 3, 8)),
        (dt.datetime(2022, 4, 1), dt.datetime(2022, 4, 8)),
        (dt.datetime(2022, 5, 1), dt.datetime(2022, 5, 8)),
        (end, end + dt.timedelta(weeks=1))
    ]
    
    return batches


def long_battle_search(dates: list, api: Twarc2, sheet: str, event: str, query: str):
    timer_start = time.time()
    n_tweets = 0
    for i,date in enumerate(dates):
        print(f"Gathering tweets for date batch {i+1} of {len(dates)}")
        res = api.search_all(
            query=query,
            start_time=date[0],
            end_time=date[1],
            max_results=100
        )
        
        for i,page in enumerate(res):
            tweets = expansions.flatten(page)
            n_tweets += len(tweets)
            
            if i % 10 == 0:
                print(f"Processing page {i}")
                print(f"Page {i} tweets: {len(tweets)}")
                print(f"Total tweets: {len(tweets) + n_tweets}")
                
            for tweet in tweets:
                with gzip.open(os.path.join("data", sheet, event, tweet["id"] + ".json.gz"), "w") as f:
                    f.write(json.dumps(tweet).encode("utf-8"))   
                    
    timer_end = time.time()
    total_time = round((timer_end - timer_start)/60, 3)
    print(f"Finished! Found {n_tweets} tweets in {total_time} minutes")
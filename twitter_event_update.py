# -*- coding: utf-8 -*-
"""
@Author: Sean Doody, START
@Email: sdoody1@umd.edu
"""
import argparse
import datetime as dt
import gzip
import json
import os
import time

import numpy as np
import pandas as pd
from tqdm import tqdm
from twarc import Twarc2, expansions

from helper_functions.long_battles import kharkiv, long_battle_search
from helper_functions.international_events import finland_sweden_nato_keywords

tqdm.pandas()

# Initialize arg parse for battles:
parser = argparse.ArgumentParser(description="START Ukraine-Russia Tweet Scraper")
parser.add_argument("-s", 
                    "--sheet_name", 
                    help="The sheet within the Excel file to pull data.")
parser.add_argument("-e", 
                    "--event_id", 
                    help="Gets tweets for the listed event.")
parser.add_argument("-d",
                    "--date_rule",
                    help="Args can be 'before' or 'after.' Will get results 1 week before or after event.")
args = parser.parse_args()


def load_events(event_path: str, sheet_name: str) -> pd.DataFrame:
    df = pd.read_excel(event_path, sheet_name=sheet_name)
    return df

def initiate_twarc():
    with open(os.path.join("credentials", "twitter-credentials.json")) as f:
        creds = json.load(f)
    
    api = Twarc2(bearer_token=creds["BEARER_TOKEN"])
    
    return api


def make_battle_keywords(battle_name: str):
    if "_" in battle_name:
        queries = [
            "(ukraine {} OR ukraine {}",
            "ukrainian {} OR ukrainian {}",
            "ukrainians {} OR ukrainians {}",
            "russia {} OR russia {}",
            "russian {} OR russian {}",
            "russians {} OR russians {}",
            "battle {} OR battle {}",
            "siege {} OR siege {}",
            "nato {} OR nato {}})"
        ]
        battle_name = battle_name.split("_")
        search_query = []
        for q in queries:
            search_query.append(q.format(battle_name[0], battle_name[1]))
        
        search_query = " OR ".join(search_query)
        search_query = search_query + " " + "lang:en -is:retweet"
        return search_query
    else:
        queries = [
            "(ukraine {}",
            "ukrainian {}",
            "ukrainians {}",
            "russia {}",
            "russian {}",
            "russians {}",
            "battle {}",
            "siege {}",
            "nato {})"
        ]
        search_query = []
        for q in queries:
            search_query.append(q.format(battle_name))
        
        search_query = " OR ".join(search_query)
        search_query = search_query + " " + "lang:en -is:retweet"
        return search_query

def make_civilian_keywords(event_name: str):
    queries = [
        "(ukraine {}",
        "ukrainian {}",
        "ukrainians {}",
        "russia {}",
        "russian {}",
        "russians {}",
        "{} massacre",
        "{} deaths",
        "{} civilians",
        "{} civilian",
        "{} killings",
        "{} killed)"
    ]
    search_query = []
    for q in queries:
        search_query.append(q.format(event_name))
    search_query = " OR ".join(search_query)
    search_query = search_query + " " + "lang:en -is:retweet"
    return search_query

def make_international_keywords(event_id: str):
    if event_id == "int09":
        search_query = finland_sweden_nato_keywords()
        search_query = " OR ".join(search_query)
        search_query = search_query + " " + "lang:en -is:retweet"
        return search_query


def main():
    assert args.sheet_name, "Error: Missing sheet name!"
    assert args.event_id, "Error: Missing event ID!"
    assert args.date_rule in ['before', 'after'], "Error: --date_rule must be 'before' or 'after'!"
    
    sheet = args.sheet_name
    event = args.event_id
    
    
    print("Loading event data")
    event_file = "ukr-events.xlsx"
    events = load_events(os.path.join("events", event_file), sheet)
    events = events.loc[events.event_id == event].to_dict("records")[0]
    
    if args.date_rule == 'before':
        events["start"] = events["date"] - dt.timedelta(weeks=1)
        events["end"] = events["date"]
    else:
        events["start"] = events["date"]
        events["end"] = events["date"] + dt.timedelta(weeks=1)
    
    start = events["start"]
    end = events["end"]
    
    print("Initializing Twarc")
    api = initiate_twarc()

    if sheet == "battles":
        query = make_battle_keywords(events["twitter_search_name"])
        if events["twitter_search_name"] == "kharkiv":
            dates = kharkiv(events["start"], events["end"])
            long_battle_search(dates, api, sheet, event, query)
    elif sheet == "civilians":
        query = make_civilian_keywords(events["twitter_search_name"])
    elif sheet == "international":
        query = make_international_keywords(args.event_id)
    
    print(f"Search query:\n{query}\n")
    
    timer_start = time.time()
    print("Beginning Twitter search")
    res = api.search_all(
        query=query,
        start_time=start,
        end_time=end,
        max_results=100
    )
    
    n_tweets = 0
    new_tweets = 0
    for i,page in enumerate(res):
        tweets = expansions.flatten(page)
        n_tweets += len(tweets)
        
        if i % 10 == 0:
            print(f"Processing page {i}")
            print(f"Page {i} tweets: {len(tweets)}")
            print(f"Total tweets: {len(tweets) + n_tweets}")
            
        for tweet in tweets:
            path = os.path.join("data", sheet, event, tweet["id"] + ".json.gz")
            # check if we already collected this tweet:
            if os.path.isfile(path):
                print(f'Tweet {tweet["id"]} already collected! Skipping.')
            else:
                new_tweets += 1
                with gzip.open(os.path.join("data", sheet, event, tweet["id"] + ".json.gz"), "w") as f:
                    f.write(json.dumps(tweet).encode("utf-8"))    
    
    timer_end = time.time()
    total_time = round((timer_end - timer_start)/60, 3)
    print(f"Finished! Found {new_tweets} new tweets out of {n_tweets} total in {total_time} minutes")
    

if __name__ == "__main__":
    main()
# -*- coding: utf-8 -*-
"""
@Author: Sean Doody, START
@Email: sdoody1@umd.edu
"""
import os
import argparse

import gzip
import json

import time
import datetime as dt

from twarc import Twarc2, expansions


def initiate_twarc():
    with open(os.path.join("credentials", "twitter-credentials.json")) as f:
        creds = json.load(f)
    
    api = Twarc2(bearer_token=creds["BEARER_TOKEN"])
    
    return api

    
def main():
    start = time.time()
    
    parser = argparse.ArgumentParser(description='START Weibo Account Message Scraper')

    parser.add_argument(
        '-a',
        '--account',
        help='The Twitter account to scrape'
    )

    parser.add_argument(
        '-d',
        '--date_cutoff',
        help='The date, in string format, to stop collecting posts'
    )

    parser_args = parser.parse_args()
    

    if not os.path.exists(os.path.join('data', 'twitter_accounts', parser_args.account)):
        print(f'No data path exists for {parser_args.account}! Creating...')
        os.mkdir(os.path.join('data', 'twitter_accounts', parser_args.account))
        os.mkdir(os.path.join('data', 'twitter_accounts', parser_args.account, 'raw'))
    
    print('Initializing Twarc')
    api = initiate_twarc()
    
    print(f'Getting Tweets for {parser_args.account}')
    query = f'from:{parser_args.account}'
    
    print(f"Search query:\n{query}\n")
    
    results = api.search_all(
        query=query,
        max_results=100
    )
    
    n_tweets = 0
    for i,page in enumerate(results):
        tweets = expansions.flatten(page)
        n_tweets += len(tweets)
        
        if i % 10 == 0:
            print(f"Processing page {i}")
            print(f"Page {i} tweets: {len(tweets)}")
            print(f"Total tweets: {len(tweets) + n_tweets}")
            
        for tweet in tweets:
            with gzip.open(os.path.join('data', 'twitter_accounts', parser_args.account, 'raw', tweet["id"] + ".json.gz"), "w") as f:
                f.write(json.dumps(tweet).encode("utf-8"))   
    
    end = time.time()
    runtime = round((end - start)/60, 3)
    
    print(f'Finished!')
    print(f'Runtime: {runtime} min. | Total Posts Scraped: {counter}')        
    
    
if __name__ == '__main__':
    main()
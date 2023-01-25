# -*- coding: utf-8 -*-
"""
@Author: Sean Doody, START
@Email: sdoody1@umd.edu
"""
import os
import time
import argparse
import datetime as dt
from tqdm import tqdm

import json
import gzip

from weibo_scraper import get_weibo_tweets_by_name


def main():
    start = time.time()

    parser = argparse.ArgumentParser(description='START Weibo Account Message Scraper')

    parser.add_argument(
        '-a',
        '--account',
        help='The Weibo account to scrape'
    )

    parser.add_argument(
        '-d',
        '--date_cutoff',
        help='The date, in epoch (int) format, to stop collecting posts'
    )

    parser_args = parser.parse_args()

    print(f'Scraping Weibo posts for {parser_args.account} | Date cutoff: {int(parser_args.date_cutoff)}')

    # initiate directory for account:
    if not os.path.exists(os.path.join('data', 'weibo', parser_args.account)):
        print(f'No data directory for account {parser_args.account}! Creating...')
        os.mkdir(os.path.join('data', 'weibo', parser_args.account))
        os.mkdir(os.path.join('data', 'weibo', parser_args.account, 'raw'))

    # Weibo date format:
    cutoff = int(parser_args.date_cutoff)
    date_format = "%a %b %d %H:%M:%S %z %Y"

    counter = 0
    for tweet in tqdm(get_weibo_tweets_by_name(name=parser_args.account, pages=None)):
        tweet_date = int(dt.datetime.strptime(tweet['mblog']['created_at'], date_format).timestamp())
        if tweet_date < cutoff:
            print(f'Tweet date ({tweet_date}) is less than cuttoff ({cutoff}): stopping collection!')
            break
        else:
            with gzip.open(
                os.path.join(
                    'data', 
                    'weibo', 
                    parser_args.account, 
                    'raw', 
                    tweet['mblog']['id'] + '.json.gz'),
                'w'
                ) as f:
                    f.write(json.dumps(tweet).encode("utf-8"))
            counter += 1

    end = time.time()
    runtime = round((end - start)/60, 3)

    print(f'Finished!')
    print(f'Runtime: {runtime} min. | Toal Posts Scraped: {counter}')        


if __name__ == '__main__':
    main()
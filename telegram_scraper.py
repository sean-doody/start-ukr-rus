# -*- coding: utf-8 -*-
'''
@Author: Sean Doody, START
@Email: sdoody1@umd.edu
'''
import os
import argparse

# Initialize parser arguments:
parser = argparse.ArgumentParser(description='START Ukraine-Russia Tweet Scraper')
parser.add_argument('-c', 
                    '--channel', 
                    help='The Telegram channel to collect posts from.')
parser.add_argument('-d', 
                    '--date_cutoff', 
                    help='The date to stop collection (YYYY-MM-DD)')
args = parser.parse_args()


def main():
    assert args.channel, 'You did not provide a channel!'
    assert args.date_cutoff, 'You did not provide a date cutoff!'
    
    if not os.path.exists(os.path.join('telegram', 'data', 'raw', args.channel)):
        output_path = os.path.join('telegram', 'data', 'raw', args.channel)
        os.mkdir(output_path)
        
        # format snscrape string:
        snscrape = f'snscrape --progress --jsonl --since {args.date_cutoff} telegram-channel {args.channel} > {output_path}/{args.channel}_data.jsonl'
        
        # execute search:
        os.system(snscrape)
    else:
        raise Exception(f'Data has already been collected for {args.channel}! Please inspect the folder.')
        

if __name__ == '__main__':
    main()
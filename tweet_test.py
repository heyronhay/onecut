#!/usr/bin/env python3
import oauth2
import json
import re

"""
A helper script to test out functionality.
"""
def oauth_req(url, key, secret, http_method="GET", post_body="", http_headers=None):
    consumer = oauth2.Consumer(key='KsB1ZcdEVzfeSyqFDhOhEt39z', secret= 'nH9U0G0KMwV0bJrtWU6v7R2tNkaarQZeQzZeWQyAdB2bcDlhwM')
    token = oauth2.Token(key=key, secret=secret)
    client = oauth2.Client(consumer, token)
    resp, content = client.request( url, method=http_method, body=bytes(post_body,"utf-8"), headers=http_headers )
    return resp, content

query='https://api.twitter.com/1.1/search/tweets.json?q=sale%20url%3Aamazon&count=100&tweet_mode=extended&result_type=recent'
for _ in range(0,1000,100):
    resp, json_str = oauth_req( query, '1364612066-ImTvXwjaSQUKlVz8yatQwn77HijKHxZ6bg2D765', '9V3Ptn8N1XQZ9y2IFSFCpcFYxByreQZoYP5KlHajsNyYT' )
    if resp['status'] == '200':
        json_str = json_str.decode('utf-8')
    #    print(json_str)
        json_data = json.loads(json_str)
        query = "https://api.twitter.com/1.1/search/tweets.json" + json_data['search_metadata']['next_results'] + "&tweet_mode=extended"
        print(query)
        tweet_subset = {}
        statuses = json_data['statuses']
        for status in statuses:
            urls = status['entities']['urls']
            if status['lang'] == 'en' and len(urls) > 0:
                tweet_subset['full_text'] = status['full_text']
                tweet_subset['amazon_url'] = urls[0]['expanded_url']
                tweet_subset['tweet_id'] = status['id']
                tweet_subset['tweet_url'] = 'https://twitter.com/statuses/{}'.format(status['id'])
                tweet_subset_str = json.dumps(tweet_subset)
                print(tweet_subset_str)
            else:
                print("Skipped tweet.")
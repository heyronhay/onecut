#!/usr/bin/env python3
import oauth2
import json

def oauth_req(url, key, secret, http_method="GET", post_body="", http_headers=None):
    consumer = oauth2.Consumer(key='KsB1ZcdEVzfeSyqFDhOhEt39z', secret= 'nH9U0G0KMwV0bJrtWU6v7R2tNkaarQZeQzZeWQyAdB2bcDlhwM')
    token = oauth2.Token(key=key, secret=secret)
    client = oauth2.Client(consumer, token)
    resp, content = client.request( url, method=http_method, body=bytes(post_body,"utf-8"), headers=http_headers )
    return resp, content

query='https://api.twitter.com/1.1/search/tweets.json?q=sale%20url%3Aamazon&count=1&result_type=recent'

resp, json_str = oauth_req( query, '1364612066-ImTvXwjaSQUKlVz8yatQwn77HijKHxZ6bg2D765', '9V3Ptn8N1XQZ9y2IFSFCpcFYxByreQZoYP5KlHajsNyYT' )
if resp['status'] == '200':
    json_str = json_str.decode('utf-8')
    print(json_str)
    json_data = json.loads(json_str)
    tweet_subset = {}
    statuses = json_data['statuses']
    if len(statuses) > 0:
        tweet_subset['text'] = json_data['statuses'][0]['text']
        urls = json_data['statuses'][0]['entities']['urls']
        if len(urls) > 0:
            tweet_subset['urls'] = urls[0]['expanded_url']
        tweet_subset_str = json.dumps(tweet_subset)

        print(tweet_subset_str)

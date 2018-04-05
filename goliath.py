import oauth2
from flask import jsonify
import json

class BirdEater:
    def __init__(self):
        self.consumer_key = 'KsB1ZcdEVzfeSyqFDhOhEt39z'
        self.consumer_secret = 'nH9U0G0KMwV0bJrtWU6v7R2tNkaarQZeQzZeWQyAdB2bcDlhwM'
        self.token_key = '1364612066-ImTvXwjaSQUKlVz8yatQwn77HijKHxZ6bg2D765'
        self.token_secret = '9V3Ptn8N1XQZ9y2IFSFCpcFYxByreQZoYP5KlHajsNyYT'

    def oauth_req(self, url, http_method="GET", post_body="", http_headers=None):
        consumer = oauth2.Consumer(key=self.consumer_key, secret=self.consumer_secret)
        token = oauth2.Token(key=self.token_key, secret=self.token_secret)
        client = oauth2.Client(consumer, token)
        resp, content = client.request(url, method=http_method, body=bytes(post_body,"utf-8"), headers=http_headers)

        return resp, content

    def add_tweets(self, count):
        query='https://api.twitter.com/1.1/search/tweets.json?q=sale%20url%3Aamazon&count={}&result_type=recent'.format(count)
        resp, tweets_json = self.oauth_req(query)
        if resp['status'] == '200':
            tweets_json = tweets_json.decode('utf-8')
            json_data = json.loads(tweets_json)
            tweet_subset = {}
            tweet_subset['text'] = json_data['statuses'][0]['text']
            tweet_subset['urls'] = json_data['statuses'][0]['entities']['urls']['expanded_url']
            tweet_subset_str = json.dumps(tweet_subset)
            resp = jsonify(tweet_subset_str)
            resp.status_code = 200
        else:
            resp = jsonify("{}")
            resp.status_code = resp['status']

        return resp


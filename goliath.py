import oauth2
from flask import jsonify, Response
import json
from redis_db import RedisDatabase
import re

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
        def add_tweet(tweet_key, urls, status):
            tweet_subset = {}
            tweet_subset['tweet_id'] = status['id']
            tweet_subset['full_text'] = str(status['full_text'])
            tweet_subset['amazon_url'] = urls[0]['expanded_url']
            tweet_subset['tweet_url'] = 'https://twitter.com/statuses/{}'.format(status['id'])
            redis_db.hmset(tweet_key, tweet_subset)
            for word in re.split('\W+', status['full_text']):
                if len(word) > 1:
                    redis_db.sadd('saleterm-{}'.format(word.lower()), tweet_key)

        query='https://api.twitter.com/1.1/search/tweets.json?q=sale%20url%3Aamazon&count={}&tweet_mode=extended&result_type=recent'.format(count)
        resp, json_str = self.oauth_req(query)

        num_tweets_added = 0
        if resp['status'] == '200':
            redis_db = RedisDatabase()

            json_data = json.loads(json_str.decode('utf-8'))
            statuses = json_data['statuses']

            for status in statuses:
                urls = status['entities']['urls']
                tweet_key = 'tweet-{}'.format(status['id'])
                if (status['lang'] == 'en' 
                        and len(urls) > 0 
                        and not redis_db.exists(tweet_key)):
                    add_tweet(tweet_key, urls, status)
                    num_tweets_added += 1

        resp = Response("Added {} tweets.".format(num_tweets_added), status=200)

        return resp

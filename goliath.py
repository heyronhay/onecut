import oauth2
from flask import jsonify, Response
import json
from redis_db import RedisDatabase
import re

class BirdEater:
    """Goliath Bird Eating Spider:  It eats tweets!"""
    def __init__(self):
        """Terrible security, will kill the twitter API app once this is over!"""
        self.consumer_key = 'KsB1ZcdEVzfeSyqFDhOhEt39z'
        self.consumer_secret = 'nH9U0G0KMwV0bJrtWU6v7R2tNkaarQZeQzZeWQyAdB2bcDlhwM'
        self.token_key = '1364612066-ImTvXwjaSQUKlVz8yatQwn77HijKHxZ6bg2D765'
        self.token_secret = '9V3Ptn8N1XQZ9y2IFSFCpcFYxByreQZoYP5KlHajsNyYT'

    def oauth_req(self, url, http_method="GET", post_body="", http_headers=None):
        """Make an autherized request to the given URL using the hardcoded keys and secrets"""
        consumer = oauth2.Consumer(key=self.consumer_key, secret=self.consumer_secret)
        token = oauth2.Token(key=self.token_key, secret=self.token_secret)
        client = oauth2.Client(consumer, token)
        resp, content = client.request(url, method=http_method, body=bytes(post_body,"utf-8"), headers=http_headers)

        return resp, content

    def add_tweets(self, count):
        """Search count tweets for 'sale' and amazon links, adding hits to redis"""
        def add_tweet(tweet_key, urls, status):
            """Help function to add a single tweet to redis"""
            tweet_subset = {}
            tweet_subset['tweet_id'] = status['id']
            tweet_subset['full_text'] = str(status['full_text'])
            tweet_subset['amazon_url'] = urls[0]['expanded_url']
            tweet_subset['tweet_url'] = 'https://twitter.com/statuses/{}'.format(status['id'])
            redis_db.hmset(tweet_key, tweet_subset)
            for word in re.split('\W+', status['full_text']):
                if len(word) > 1:
                    redis_db.sadd('saleterm-{}'.format(word.lower()), tweet_key)
            status_id_num = int(status['id'])
            redis_db.sadd('all_tweets', status_id_num)
            curr_max = int(redis_db.get('tweet_max_id'))
            if status_id_num > curr_max:
                redis_db.set('tweet_max_id', status_id_num)
            curr_min = int(redis_db.get('tweet_min_id'))
            if status_id_num < curr_min:
                redis_db.set('tweet_min_id', status_id_num)
            redis_db.incr('tweet_count')
                

        redis_db = RedisDatabase()

        # Put in a notification entry into redis to signify the data is being loaded
        redis_db.set("tweet_db_status", "loading")
        query='https://api.twitter.com/1.1/search/tweets.json?q=sale%20url%3Aamazon&count=100&tweet_mode=extended&result_type=recent'

        # Twitter api only returns max 100 tweets at a time, so iterate by 100 up to count.
        num_tweets_added = 0
        for _ in range(0,count,100):
            resp, json_str = self.oauth_req(query)

            if resp['status'] == '200':
                json_data = json.loads(json_str.decode('utf-8'))
                if 'next_results' not in json_data['search_metadata']:
                    # There are no more tweets to get according to twitter, so stop trying.
                    break
                query = "https://api.twitter.com/1.1/search/tweets.json" + json_data['search_metadata']['next_results'] + "&tweet_mode=extended"
                statuses = json_data['statuses']

                for status in statuses:
                    urls = status['entities']['urls']
                    tweet_key = 'tweet-{}'.format(status['id'])
                    if (status['lang'] == 'en' 
                            and len(urls) > 0 
                            and not redis_db.exists(tweet_key)):
                        add_tweet(tweet_key, urls, status)
                        num_tweets_added += 1

        # tweet_db_status can be used to see if tweets have been loaded.
        redis_db.set("tweet_db_status", "loaded")

        return num_tweets_added


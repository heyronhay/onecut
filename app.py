#!/usr/bin/env python3

from flask import Flask, request
import oauth2
import os
import redis
from redis_db import RedisDatabase
from goliath import BirdEater
import re
from flask import jsonify, Response
import sys

app = Flask(__name__)

# Initialize redis, and add some default keys.
redis_db = RedisDatabase()
redis_db.set('tweet_count', 0)
redis_db.set('tweet_max_id', -1)
redis_db.set('tweet_min_id', sys.maxsize)

# "Bird Eating Goliath Spider":  It eats tweets
tweet_scraper = BirdEater()
default_num_tweets_to_try = 1000

@app.route('/')
def hello_world():
    """Simple test to make sure the API is working"""
    resp_dict = {}
    resp_dict['hello_world'] = 'onecut is live!'
    resp = jsonify(resp_dict)
    resp.status_code = 200
    return resp

@app.route('/tweet_count')
def tweet_count():
    """Return number of tweets in redis"""
    resp_dict = {}
    resp_dict['tweet_count'] = redis_db.get("tweet_count")
    resp = jsonify(resp_dict)
    resp.status_code = 200
    return resp

@app.route('/tweet_max_id')
def tweet_max_id():
    """Return the maximum tweet id in redis"""
    resp_dict = {}
    resp_dict['tweet_max_id'] = redis_db.get("tweet_max_id")
    resp = jsonify(resp_dict)
    resp.status_code = 200
    return resp

@app.route('/tweet_min_id')
def tweet_min_id():
    """Return the minimum tweet id in redis"""
    resp_dict = {}
    resp_dict['tweet_min_id'] = redis_db.get("tweet_min_id")
    resp = jsonify(resp_dict)
    resp.status_code = 200
    return resp


@app.route('/query', methods=['GET','POST'])
def query():
    """Perform a query on the dataset, where the search terms are given by the saleterm parameter"""
    # If redis hasn't been populated, stick some tweet data into it.
    if redis_db.get("tweet_db_status") != "loaded":
        tweet_scraper.add_tweets(default_num_tweets_to_try)

    sale_term = request.form['saleterm']
    subterms = re.split('\W+', sale_term)
    saleterm_keys = ['saleterm-{}'.format(w) for w in subterms if len(w) > 1]
    result_dict = {}
    num_tweets = 0
    if saleterm_keys:
        common_tweet_ids = redis_db.sinter(saleterm_keys)
        if common_tweet_ids:
            result_dict['tweets'] = [redis_db.hgetall(tweet_id) for tweet_id in common_tweet_ids]
            num_tweets = len(common_tweet_ids)

    result_dict['num_tweets'] = num_tweets
    result_dict['saleterm'] = sale_term
    resp = jsonify(result_dict)
    resp.status_code = 200
    return resp

@app.route('/redis_test')
def redis_test():
    """Test to see if redis is up"""
    redis_db.set("test",999)
    resp = Response(redis_db.get("test"), status=200)

    return resp

@app.route('/load_tweets', methods=['GET','POST'])
def tweet():
    """Try to load a number of tweets given by the parameter 'num_tweets_to_try'"""
    num_tweets_to_try = default_num_tweets_to_try
    if 'num_tweets_to_try' in request.form:
        num_tweets_to_try = int(request.form['num_tweets_to_try'])

    tweet_scraper.add_tweets(num_tweets_to_try)

    resp_dict = {}
    resp_dict['tweet_count'] = redis_db.get("tweet_count")
    resp_dict['tweet_min_id'] = redis_db.get("tweet_min_id")
    resp_dict['tweet_max_id'] = redis_db.get("tweet_max_id")
    resp = jsonify(resp_dict)
    resp.status_code = 200

    return resp

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')


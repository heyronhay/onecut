#!/usr/bin/env python3

from flask import Flask, request
import oauth2
import os
import redis
from redis_db import RedisDatabase
from goliath import BirdEater
import re
from flask import jsonify, Response

app = Flask(__name__)
redis_db = RedisDatabase()
tweet_scraper = BirdEater()

@app.route('/')
def hello_world():
    return 'Flask Dockerized'

@app.route('/query', methods=['GET','POST'])
def query():
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
    redis_db.set("test",999)
    return redis_db.get("test")

@app.route('/tweet')
def tweet():
    return tweet_scraper.add_tweets(10)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')


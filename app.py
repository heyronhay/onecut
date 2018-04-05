#!/usr/bin/env python3

from flask import Flask
from flask import request
import oauth2
import os
import redis
from redis_db import RedisDatabase
from goliath import BirdEater

app = Flask(__name__)
redis_db = RedisDatabase()
tweet_scraper = BirdEater()

@app.route('/')
def hello_world():
    return 'Flask Dockerized'

@app.route('/query', methods=['GET','POST'])
def query():
    return 'Query user = {}\n'.format(request.form['user'])

@app.route('/redis_test')
def redis_test():
    redis_db.set("test",999)
    return redis_db.get("test")

@app.route('/tweet')
def tweet():
    return tweet_scraper.add_tweets(1)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')


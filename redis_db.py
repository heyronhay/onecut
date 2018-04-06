#!/usr/bin/env python3

import os
import redis

class RedisDatabase:
    def __init__(self):
        redis_host = os.environ.get('REDIS_HOST', '127.0.0.1')
        redis_port = os.environ.get('REDIS_PORT', 6379)

        self.db = redis.StrictRedis(host=redis_host, port=redis_port)

    def set(self, key, value):
        self.db.set(key, value)

    def get(self, key):
        value = self.db.get(key)
        return None if not value else value.decode('utf-8')
    
    def exists(self, key):
        return self.db.exists(key) == 1

    def hmset(self, key, dict):
        self.db.hmset(key, dict)

    def hgetall(self, key):
        value_dict = self.db.hgetall(key)
        return None if not value_dict else {key.decode('utf-8'):value.decode('utf-8') for key,value in value_dict.items()}

    def sadd(self, key, value):
        self.db.sadd(key, value)
    
    def smembers(self, key):
        self.db.smembers(key)

    def sinter(self, keys):
        value = self.db.sinter(keys)
        return None if not value else [v.decode('utf-8') for v in value]
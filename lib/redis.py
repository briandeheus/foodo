import redis
import os

REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
_c = redis.Redis(host=REDIS_HOST)

_c.ping()


def get_connection():
    return _c

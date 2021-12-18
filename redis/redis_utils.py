import redis
from mongodb.query_manager import *
import bson.json_util as json_util

class Cache:
    def __init__(self):
        self.conn = redis.Redis(host='192.168.1.2', port=6379)

    def get_user(self, uid):
        return self.conn.get(f'user_{uid}').decode('utf-8')

    def set_user(self, uid, json):
        return self.conn.set(f'user_{uid}', json)


if __name__ == '__main__':
    cache = Cache()
    res = QueryManager.query_user({'uid': '1'})
    cache.set_user(res[0]['uid'], json_util.dumps(res[0]))
    print(json_util.loads(cache.get_user('1')))
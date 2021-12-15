from config import *

class QueryManager:
    @classmethod
    def query_user(self, query, field={}):
        cols = list(MongoCollections.user().values())
        return list(cols[0].find(query, field)) + list(cols[1].find(query, field))

    @classmethod
    def query_one_user(self, query, field={}):
        cols = list(MongoCollections.user().values())
        result = list(cols[0].find(query, field)) + list(cols[1].find(query, field))
        return result[0]

    @classmethod
    def query_article(self, query, field={}):
        cols = list(MongoCollections.article().values())
        return list(cols[0].find(query, field)) + list(cols[1].find(query, field))

    @classmethod
    def query_read(self, query, field={}):
        cols = list(MongoCollections.read().values())
        return list(cols[0].find(query, field)) + list(cols[1].find(query, field))
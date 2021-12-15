from config import *

class QueryManager:
    @classmethod
    def query_user(self, query):
        cols = list(MongoCollections.user().values())
        return list(cols[0].find(query)) + list(cols[1].find(query))

    @classmethod
    def query_article(self, query):
        cols = list(MongoCollections.article().values())
        return list(cols[0].find(query)) + list(cols[1].find(query))

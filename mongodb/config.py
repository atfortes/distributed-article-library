import pymongo.cursor
from pymongo import MongoClient
from query_manager import *
import json


class MongoConn:
    @classmethod
    def connect(self):
        return MongoClient('localhost', 60000)


class MongoDatabase:
    @classmethod
    def database(self):
        return MongoConn.connect().demo


class MongoCollections:
    @classmethod
    def user(self):
        return {'Beijing': MongoDatabase.database().user_beijing,
                'Hong Kong': MongoDatabase.database().user_hong_kong}

    @classmethod
    def article(self):
        return {'science': MongoDatabase.database().article_science,
                'technology': MongoDatabase.database().article_tech}


class MongoInit:
    def __init__(self):
        self.root_dir = '../python-generate-3-sized-datasets_new/'
        self.user_path = 'user.dat'
        self.article_path = 'article.dat'
        self.read_path = 'read.dat'

    def init_user(self):
        user_file = open(self.root_dir + self.user_path, 'r')
        for line in user_file.readlines():
            entry = json.loads(line)
            MongoCollections.user()[entry['region']].insert_one(entry)
        user_file.close()

    def init_article(self):
        article_file = open(self.root_dir + self.article_path, 'r')
        for line in article_file.readlines():
            entry = json.loads(line)
            MongoCollections.article()[entry['category']].insert_one(entry)
        article_file.close()

    def init_read(self):
        read_file = open(self.root_dir + self.read_path, 'r')
        for line in read_file.readlines():
            entry = json.loads(line)
            MongoCollections.user()[entry.region].insert_one(entry)
        read_file.close()

    def init_all(self):
        self.init_user()
        self.init_article()
        self.init_read()


if __name__ == '__main__':
    print(QueryManager.query_user({'uid': '1'}))
    '''init = MongoInit()
    init.init_article()'''

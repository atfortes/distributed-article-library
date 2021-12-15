from pymongo import InsertOne, DeleteMany, ReplaceOne, UpdateOne
from pymongo import MongoClient
from query_manager import *
import numpy as np
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

    @classmethod
    def read(self):
        return {'Beijing': MongoDatabase.database().read_beijing,
                'Hong Kong': MongoDatabase.database().read_hong_kong}


class MongoInit:
    def __init__(self):
        self.root_dir = '../python-generate-3-sized-datasets_new/'
        self.user_path = 'user.dat'
        self.article_path = 'article.dat'
        self.read_path = 'read.dat'
        self.bulk_size = 10000
        self.bulk_size_read = 50000

    def init_user(self):
        user_file = open(self.root_dir + self.user_path, 'r')
        bulk_counter, bulk_dict = 0, {'Beijing': [], 'Hong Kong': []}
        for line in user_file.readlines():
            bulk_counter += 1
            doc = json.loads(line)
            bulk_dict[doc['region']] += [InsertOne(doc)]
            if bulk_counter == self.bulk_size:
                MongoCollections.user()['Beijing'].bulk_write(bulk_dict['Beijing'], ordered=True)
                MongoCollections.user()['Hong Kong'].bulk_write(bulk_dict['Hong Kong'], ordered=True)
                bulk_counter = 0
                bulk_dict['Beijing'], bulk_dict['Hong Kong'] = [], []
        if bulk_dict['Beijing']:
            MongoCollections.user()['Beijing'].bulk_write(bulk_dict['Beijing'], ordered=True)
        if bulk_dict['Hong Kong']:
            MongoCollections.user()['Hong Kong'].bulk_write(bulk_dict['Hong Kong'], ordered=True)
        user_file.close()

    def init_article(self):
        article_file = open(self.root_dir + self.article_path, 'r')
        bulk_counter, bulk_dict = 0, {'science': [], 'technology': []}
        for line in article_file.readlines():
            bulk_counter += 1
            doc = json.loads(line)
            bulk_dict[doc['category']] += [InsertOne(doc)]
            if bulk_counter == self.bulk_size:
                MongoCollections.article()['science'].bulk_write(bulk_dict['science'], ordered=True)
                MongoCollections.article()['technology'].bulk_write(bulk_dict['technology'], ordered=True)
                bulk_counter = 0
                bulk_dict['science'], bulk_dict['technology'] = [], []
        if bulk_dict['science']:
            MongoCollections.article()['science'].bulk_write(bulk_dict['science'], ordered=True)
        if bulk_dict['technology']:
            MongoCollections.article()['technology'].bulk_write(bulk_dict['technology'], ordered=True)
        article_file.close()

    def init_read(self):
        read_file = open(self.root_dir + self.read_path, 'r')
        bulk_counter, bulk_list, uids = 0, [], []
        for line in read_file.readlines():
            bulk_counter += 1
            doc = json.loads(line)
            uids += [doc['uid']]
            bulk_list += [InsertOne(doc)]
            if bulk_counter == self.bulk_size_read:
                regions = QueryManager.query_user({'uid': {'$in': uids}}, {'uid': 1, 'region': 1})
                regions = dict(map(lambda x: (x['uid'], x['region']), regions))
                regions = list(map(lambda x: regions[x], uids))
                beijing_index = np.argwhere(np.array(regions) == 'Beijing').reshape(-1)
                hk_index = np.argwhere(np.array(regions) == 'Hong Kong').reshape(-1)
                bulk_list = np.array(bulk_list)
                MongoCollections.read()['Beijing'].bulk_write(list(bulk_list[beijing_index]), ordered=True)
                MongoCollections.read()['Hong Kong'].bulk_write(list(bulk_list[hk_index]), ordered=True)
                bulk_counter = 0
                bulk_list, uids = [], []
        if bulk_counter > 0:
            regions = QueryManager.query_user({'uid': {'$in': uids}}, {'uid': 1, 'region': 1})
            regions = dict(map(lambda x: (x['uid'], x['region']), regions))
            regions = list(map(lambda x: regions[x], uids))
            beijing_index = np.argwhere(np.array(regions) == 'Beijing').reshape(-1)
            hk_index = np.argwhere(np.array(regions) == 'Hong Kong').reshape(-1)
            bulk_list = np.array(bulk_list)
            MongoCollections.read()['Beijing'].bulk_write(list(bulk_list[beijing_index]), ordered=True)
            MongoCollections.read()['Hong Kong'].bulk_write(list(bulk_list[hk_index]), ordered=True)
        read_file.close()

    def init_all(self):
        print('Initializing user collection...\n')
        self.init_user()
        print('Initializing article collection...\n')
        self.init_article()
        print('Initializing read collection...\n')
        self.init_read()


if __name__ == '__main__':
    init = MongoInit()
    init.init_all()

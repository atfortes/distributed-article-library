from pymongo import InsertOne, DeleteMany, ReplaceOne, UpdateOne
from query_manager import *
from user import *
from article import *
from read import *
from be_read import *
import numpy as np
import json


class MongoInit:
    def __init__(self):
        self.root_dir = '../python-generate-3-sized-datasets_new/'
        self.user_path = 'user.dat'
        self.article_path = 'article.dat'
        self.read_path = 'read.dat'
        self.bulk_size = 10000
        self.bulk_size_read = 50000

    def init_user(self):
        print('Initializing user collection...\n')
        user_file = open(self.root_dir + self.user_path, 'r')
        bulk_counter, bulk_dict = 0, {'Beijing': [], 'Hong Kong': []}
        for line in user_file.readlines():
            bulk_counter += 1
            doc = json.loads(line)
            bulk_dict[doc['region']] += [InsertOne(doc)]
            if bulk_counter == self.bulk_size:
                User.bulk_write(bulk_dict)
                bulk_counter = 0
                bulk_dict['Beijing'], bulk_dict['Hong Kong'] = [], []
        if bulk_counter > 0:
            User.bulk_write(bulk_dict)
        user_file.close()

    def init_article(self):
        print('Initializing article collection...\n')
        article_file = open(self.root_dir + self.article_path, 'r')
        bulk_counter, bulk_dict = 0, {'science': [], 'technology': []}
        for line in article_file.readlines():
            bulk_counter += 1
            doc = json.loads(line)
            bulk_dict[doc['category']] += [InsertOne(doc)]
            if bulk_counter == self.bulk_size:
                Article.bulk_write(bulk_dict)
                bulk_counter = 0
                bulk_dict['science'], bulk_dict['technology'] = [], []
        if bulk_counter > 0:
            Article.bulk_write(bulk_dict)
        article_file.close()

    def init_read(self):
        print('Initializing read collection...\n')
        read_file = open(self.root_dir + self.read_path, 'r')
        bulk_counter, bulk_list, uids = 0, [], []
        be_read_docs_dict = {}
        for line in read_file.readlines():
            bulk_counter += 1
            doc = json.loads(line)
            uids += [doc['uid']]
            bulk_list += [InsertOne(doc)]
            if not doc['aid'] in be_read_docs_dict:
                be_read_docs_dict[doc['aid']] = self.create_be_read_doc(
                    doc['aid'], doc['uid'], int(doc['commentOrNot']), int(doc['agreeOrNot']), int(doc['shareOrNot'])
                )
            if doc['aid'] in be_read_docs_dict:
                be_read_docs_dict[doc['aid']] = self.increment_be_read_doc(
                    be_read_docs_dict[doc['aid']], doc['uid'], int(doc['commentOrNot']), int(doc['agreeOrNot']), int(doc['shareOrNot'])
                )
            if bulk_counter == self.bulk_size_read:
                regions = QueryManager.query_user({'uid': {'$in': uids}}, {'uid': 1, 'region': 1})
                regions = dict(map(lambda x: (x['uid'], x['region']), regions))
                regions = list(map(lambda x: regions[x], uids))
                beijing_index = np.argwhere(np.array(regions) == 'Beijing').reshape(-1)
                hk_index = np.argwhere(np.array(regions) == 'Hong Kong').reshape(-1)
                Read.bulk_write({'Beijing': np.array(bulk_list)[beijing_index],
                                  'Hong Kong': np.array(bulk_list)[hk_index]})
                self.init_be_read(be_read_docs_dict)
                bulk_counter, bulk_list, uids = 0, [], []
        if bulk_counter > 0:
            regions = QueryManager.query_user({'uid': {'$in': uids}}, {'uid': 1, 'region': 1})
            regions = dict(map(lambda x: (x['uid'], x['region']), regions))
            regions = list(map(lambda x: regions[x], uids))
            beijing_index = np.argwhere(np.array(regions) == 'Beijing').reshape(-1)
            hk_index = np.argwhere(np.array(regions) == 'Hong Kong').reshape(-1)
            Read.bulk_write({'Beijing': np.array(bulk_list)[beijing_index],
                              'Hong Kong': np.array(bulk_list)[hk_index]})
            self.init_be_read(be_read_docs_dict)
        read_file.close()

    def init_be_read(self, docs_dict):
        bulk_list = []
        categories = QueryManager.query_user({'uid': {'$in': list(docs_dict.keys())}}, {'aid': 1, 'category': 1})
        categories = dict(map(lambda x: (x['aid'], x['category']), categories))
        categories = list(map(lambda x: categories[x], docs_dict.keys()))
        science_index = np.argwhere(np.array(categories) == 'science').reshape(-1)
        tech_index = np.argwhere(np.array(categories) == 'technology').reshape(-1)
        for aid in docs_dict:
            res = QueryManager.query_be_read({'aid': aid})
            if res:
                bulk_list += [UpdateOne(self.sum_be_read_docs(res[0], docs_dict[aid]))]
            else:
                bulk_list += [InsertOne(docs_dict[aid])]
        Read.bulk_write({'science': np.array(bulk_list)[science_index],
                         'technology': np.array(bulk_list)[tech_index]})

    def create_be_read_doc(self, aid, uid, comment, agree, share):
        comList, aggList, shrList = [], [], []
        if comment:
            comList = [uid, ]
        if agree:
            aggList = [uid, ]
        if share:
            shrList = [uid, ]
        return {
                    'id': f'br{aid}',
                    'timestamp': Collection.get_current_timestamp(),
                    'aid': aid,
                    'readNum': '1',
                    'readUidList': [uid, ],
                    'commentNum': str(comment),
                    'commentUidList': comList,
                    'agreeNum': str(agree),
                    'agreeUidList': aggList,
                    'shareNum': str(share),
                    'shareUidList': shrList,
                }

    def increment_be_read_doc(self, current_doc, uid, comment, agree, share):
        incremented_doc = current_doc
        incremented_doc['readNum'] = str(int(incremented_doc['readNum']) + 1)
        incremented_doc['readUidList'] += [uid]
        if comment:
            incremented_doc['commentNum'] = str(int(incremented_doc['commentNum']) + 1)
            incremented_doc['commentUidList'] += [uid]
        if agree:
            incremented_doc['commentNum'] = str(int(incremented_doc['commentNum']) + 1)
            incremented_doc['commentUidList'] += [uid]
        if share:
            incremented_doc['shareNum'] = str(int(incremented_doc['shareNum']) + 1)
            incremented_doc['shareUidList'] += [uid]
        return incremented_doc

    def sum_be_read_docs(self, doc1, doc2):
        return {
                    'id': doc1['id'],
                    'timestamp': Collection.get_current_timestamp(),
                    'aid': doc1['aid'],
                    'readNum': str(int(doc1['readNum']) + int(doc2['readNum'])),
                    'readUidList': doc1['readUidList'] + doc2['readUidList'],
                    'commentNum': str(int(doc1['commentNum']) + int(doc2['commentNum'])),
                    'commentUidList': doc1['commentUidList'] + doc2['commentUidList'],
                    'agreeNum': str(int(doc1['agreeNum']) + int(doc2['agreeNum'])),
                    'agreeUidList': doc1['agreeUidList'] + doc2['agreeUidList'],
                    'shareNum': str(int(doc1['shareNum']) + int(doc2['shareNum'])),
                    'shareUidList': doc1['shareUidList'] + doc2['shareUidList'],
                }

    def init_all(self):
        self.init_user()
        self.init_article()
        self.init_read()


if __name__ == '__main__':
    init = MongoInit()
    init.init_all()

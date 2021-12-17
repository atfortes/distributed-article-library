from mongodb.config import *


class QueryManager:
    @classmethod
    def query_user(self, query={}, field={}):
        cols = list(User.user().values())
        return list(cols[0].find(query, field)) + list(cols[1].find(query, field))

    @classmethod
    def query_one_user(self, query={}, field={}):
        cols = list(User.user().values())
        result = list(cols[0].find(query, field)) + list(cols[1].find(query, field))
        return result[0]

    @classmethod
    def query_article(self, query={}, field={}):
        cols = list(Article.article().values())
        return list(cols[0].find(query, field)) + list(cols[1].find(query, field))

    @classmethod
    def query_read(self, query={}, field={}):
        cols = list(Read.read().values())
        return list(cols[0].find(query, field)) + list(cols[1].find(query, field))

    @classmethod
    def query_be_read(self, query={}, field={}):
        cols = list(BeRead.be_read().values())
        return list(cols[0].find(query, field)) + list(cols[1].find(query, field))

    @classmethod
    def query_popular_rank(self, query={}, field={}):
        cols = list(PopularRank.popular_rank().values())
        return list(cols[0].find(query, field)) + list(cols[1].find(query, field)) + list(cols[2].find(query, field))

    @classmethod
    def query_join_read_user(self, query={}, field={}):
        cols = list(Read.read().values())
        read_res = list(cols[0].find(query, field)) + list(cols[1].find(query, field))
        uids = list(set(map(lambda x: x['uid'], read_res)))
        user_res = self.query_user({'uid': {'$in': uids}})
        users = dict(map(lambda x: (x['uid'], x), user_res))
        for read in read_res:
            read['user'] = users[read['uid']]
        return read_res

    @classmethod
    def query_join_user_read(self, query={}, field={}):
        cols = list(User.user().values())
        user_res = list(cols[0].find(query, field)) + list(cols[1].find(query, field))
        uids = list(set(map(lambda x: x['uid'], user_res)))
        read_res = self.query_read({'uid': {'$in': uids}})
        read_uid = {}
        for read in read_res:
            if not read['uid'] in read_uid:
                read_uid[read['uid']] = [read]
            else:
                read_uid[read['uid']] += [read]
        for user in user_res:
            user['reads'] = read_uid[user['uid']]
        return user_res

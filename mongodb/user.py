from collection import *


class User(Collection):
    @classmethod
    def user(cls):
        return {'Beijing': MongoDatabase.database().user_beijing,
                'Hong Kong': MongoDatabase.database().user_hong_kong}

    @classmethod
    def bulk_write(cls, bulk_dict):
        User.user()['Beijing'].bulk_write(bulk_dict['Beijing'], ordered=True)
        User.user()['Hong Kong'].bulk_write(bulk_dict['Hong Kong'], ordered=True)

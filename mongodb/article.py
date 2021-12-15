from collection import *


class Article(Collection):
    @classmethod
    def article(cls):
        return {'science': MongoDatabase.database().article_science,
                'technology': MongoDatabase.database().article_tech}

    @classmethod
    def bulk_write(cls, bulk_dict):
        Article.article()['science'].bulk_write(bulk_dict['science'], ordered=True)
        Article.article()['technology'].bulk_write(bulk_dict['technology'], ordered=True)

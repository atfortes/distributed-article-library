from pymongo import MongoClient
import ast

root_dir = "../python-generate-3-sized-datasets_new/"

if __name__ == '__main__':
      conn = MongoClient('localhost', 60000)
      db = conn.demo
      user_col = db.user
      article_col = db.article

      '''users_file = open(root_dir + "user.dat", "r")
      line = users_file.readline()
      while line:
            entry = ast.literal_eval(line.replace("\n", ""))
            x = user_col.insert_one(entry)
            line = users_file.readline()
      users_file.close()'''

      article_file = open(root_dir + "article.dat", "r")
      line = article_file.readline()
      while line:
            entry = ast.literal_eval(line.replace("\n", ""))
            x = article_col.insert_one(entry)
            line = article_file.readline()
      article_file.close()





import os
import pyhdfs

HOST='localhost'
PORT='9870'
ARTICLES_PATH='/user/root/articles/'

class HadoopManager:

    def __init__(self, HOST: str, PORT: str, user_name='root') -> None:
        self.client = pyhdfs.HdfsClient(hosts=[
            f'{HOST}:{PORT}',
            f'{HOST}:{9866}',
            f'{HOST}:{9864}'
            ], user_name=user_name)

    def exists(self, path: str) -> bool:
        return self.client.exists(ARTICLES_PATH + path)

    def list_status(self, path) -> list:
        return self.client.list_status(ARTICLES_PATH + path)

    def content_summary(self, path):
        return self.client.get_content_summary(ARTICLES_PATH + path)

    def read_file(self, article, file_name) -> bytes:
        with self.client.open(ARTICLES_PATH + article + '/' + file_name) as f:
            print(f)

    def create_file(self, article: str, file_name: str, data: bytes) -> None:
        self.client.create(ARTICLES_PATH + article + '/' + file_name, data)

    def delete_file(self, article: str, file_name: str) -> None:
        self.client.delete(ARTICLES_PATH + article + '/' + file_name)

    def upload_file(self, source_path: str, article: str, file_name: str) -> None:
        self.client.copy_from_local(source_path, ARTICLES_PATH + article + '/' + file_name)

    def download_file(self, article: str, file_name: str, dest_path: str, ) -> None:
        self.client.copy_to_local(ARTICLES_PATH + article + '/' + file_name, dest_path)

    def list_article(self, article: str) -> list:
        return self.client.listdir(ARTICLES_PATH + article + '/')

    def read_article(self, article) -> dict:
        files = {}
        for file in self.list_article(article):
            files[file] = self.read_file(article, file)
        return files

    def upload_article(self, source_path, article) -> None:
        path = ARTICLES_PATH + article
        if not self.exits(path):
            self.client.mkdirs(path)
            for source_file in os.listdir(source_path):
                self.upload_file(source_file, article, source_file.split('/')[-1])

    def delete_article(self, article) -> None:
        files = self.list_article(article)
        for file in files:
            self.delete_file(article, file)


if __name__ == "__main__":
    hdfs = HadoopManager(HOST, PORT)
    print(hdfs.read_file('article0', 'text_a0.txt'))

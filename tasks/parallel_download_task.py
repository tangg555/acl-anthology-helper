"""
@Desc:
"""
import os
from src.modules import Retriever
from src.modules.parallel_downloader import PaperDownloader

class ParallelDownloadTask(object):
    @classmethod
    def acl_long_download(cls, key_word: str):
        conf_content = '2021-acl-long'
        papers = Retriever.acl(2021, conf_content, True)  # use local cache
        downloader = PaperDownloader()

        filtered = papers.filter('title', key_word) | papers.filter('abstract', key_word)
        downloader.multi_download(filtered, os.path.join(key_word, conf_content))

    @classmethod
    def naacl_main_download(cls, key_word: str):
        conf_content = '2021-naacl-main'
        papers = Retriever.naacl(2021, conf_content, True)  # use local cache
        downloader = PaperDownloader()

        filtered = papers.filter('title', key_word) | papers.filter('abstract', key_word)
        downloader.multi_download(filtered, os.path.join(key_word, conf_content))

    @classmethod
    def emnlp_main_download(cls, key_word: str):
        conf_content = '2020-emnlp-main'
        papers = Retriever.emnlp(2020, conf_content, True)  # use local cache
        downloader = PaperDownloader()

        filtered = papers.filter('title', key_word) | papers.filter('abstract', key_word)
        downloader.multi_download(filtered, os.path.join(key_word, conf_content))

    @classmethod
    def run(cls):
        while True:
            keyword = input('type a keyword(blank will exit): ')
            if not keyword.strip():
                break
            cls.acl_long_download(keyword)
            cls.naacl_main_download(keyword)
            cls.emnlp_main_download(keyword)


if __name__ == '__main__':
    ParallelDownloadTask.run()

"""
@Desc:
"""
import sys
sys.path.insert(0, '..') # 在tasks文件夹中可以直接运行程序

import os
from src.modules import Retriever
from src.modules.parallel_downloader import PaperDownloader


class ParallelDownloadTask(object):
    @classmethod
    def acl_long_download(cls, keyword: str):
        conf_content = '2021-acl-long'
        papers = Retriever.acl(2021, conf_content, True)  # use local cache
        downloader = PaperDownloader()

        filtered = papers.containing_filter('title', keyword) | papers.containing_filter('abstract', keyword)
        downloader.multi_download(filtered, os.path.join(keyword, conf_content))

    @classmethod
    def naacl_main_download(cls, keyword: str):
        conf_content = '2021-naacl-main'
        papers = Retriever.naacl(2021, conf_content, True)  # use local cache
        downloader = PaperDownloader()

        filtered = papers.containing_filter('title', keyword) | papers.containing_filter('abstract', keyword)
        downloader.multi_download(filtered, os.path.join(keyword, conf_content))

    @classmethod
    def emnlp_main_download(cls, keyword: str):
        conf_content = '2020-emnlp-main'
        papers = Retriever.emnlp(2020, conf_content, True)  # use local cache
        downloader = PaperDownloader()

        filtered = papers.containing_filter('title', keyword) | papers.containing_filter('abstract', keyword)
        downloader.multi_download(filtered, os.path.join(keyword, conf_content))

    @classmethod
    def run(cls):
        while True:
            keyword = input('\ntype a keyword(blank will exit): ')
            if not keyword.strip():
                break
            cls.acl_long_download(keyword)
            cls.naacl_main_download(keyword)
            cls.emnlp_main_download(keyword)


if __name__ == '__main__':
    ParallelDownloadTask.run()

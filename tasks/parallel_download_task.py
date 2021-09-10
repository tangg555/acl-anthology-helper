"""
@Desc:
"""
import os
from src.modules import Retriever
from src.modules.constants import ACLConsts, NAACLConsts
from src.modules.parallel_downloader import PaperDownloader

class ParallelDownloadTask(object):
    @classmethod
    def acl_long_download(cls):
        papers = Retriever.acl(2021, ACLConsts.LONG, True)  # use local cache
        downloader = PaperDownloader()

        filtered = papers.filter('title', 'commonsense') | papers.filter('abstract', 'commonsense')
        downloader.multi_download(filtered, os.path.join(ACLConsts.LONG, 'multi_download'))

    @classmethod
    def naacl_long_download(cls):
        papers = Retriever.naacl(2021, NAACLConsts.MAIN, True)  # use local cache
        downloader = PaperDownloader()

        filtered = papers.filter('title', 'commonsense') | papers.filter('abstract', 'commonsense')
        downloader.multi_download(filtered, os.path.join(NAACLConsts.MAIN, 'multi_download'))

    @classmethod
    def run(cls):
        cls.naacl_long_download()


if __name__ == '__main__':
    ParallelDownloadTask.run()

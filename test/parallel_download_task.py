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
        acl = Retriever.acl(2021, ACLConsts.LONG, True)    # use local cache
        downloader = PaperDownloader()

        papers = acl.papers
        filtered = papers.filter('title', 'commonsense') | papers.filter('abstract', 'commonsense')
        downloader.multi_download(filtered, os.path.join(acl.conf_content, 'multi_download'))

    @classmethod
    def naacl_long_download(cls):
        naacl = Retriever.naacl(2021, NAACLConsts.MAIN, True)  # use local cache
        downloader = PaperDownloader()

        papers = naacl.papers
        filtered = papers.filter('title', 'commonsense') | papers.filter('abstract', 'commonsense')
        downloader.multi_download(filtered, os.path.join(naacl.conf_content, 'multi_download'))

    @classmethod
    def run(cls):
        cls.naacl_long_download()

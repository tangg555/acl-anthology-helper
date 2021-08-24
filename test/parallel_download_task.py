"""
@Desc:
"""
import os
from src.modules import Retriever
from src.modules.constants import ConfConsts
from src.modules.parallel_downloader import PaperDownloader


class ParallelDownloadTask(object):
    @classmethod
    def run(cls):
        acl = Retriever.acl(2021, ConfConsts.LONG, True)    # use local cache
        downloader = PaperDownloader()

        papers = acl.papers
        filtered = papers.filter('title', 'commonsense') | papers.filter('abstract', 'commonsense')
        downloader.multi_download(filtered, os.path.join(acl.conf_content, 'multi_download'))

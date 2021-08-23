"""
@Desc:
"""
import os
from src.modules import Retriever
from src.modules.constants import ConfConsts
from src.modules.downloader import PaperDownloader


class BaseTask(object):
    @classmethod
    def run(cls):
        acl = Retriever.acl(2021, ConfConsts.LONG, True)    # use local cache
        downloader = PaperDownloader()

        papers = acl.papers
        filtered = papers.filter('title', 'commonsense') | papers.filter('abstract', 'commonsense')
        downloader.multi_download(filtered, os.path.join(acl.conf_content, 'commonsense_title_or_abstract'))

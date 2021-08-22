"""
@Desc:
"""

from src.modules import Retriever
from src.modules.constants import ConfConsts
from src.modules.downloader import PaperDownloader


class BaseTask(object):
    @classmethod
    def run(cls):
        acl = Retriever.acl(2021, ConfConsts.LONG)
        downloader = PaperDownloader()

        papers = acl.papers
        filtered = papers.filter('title', 'commonsense')
        downloader.multi_download(filtered, acl.conf_content, True)

"""
@Desc:
"""
import os
from src.modules import Retriever
from src.modules.constants import ACLConsts
from src.modules.downloader import PaperDownloader
from src.modules.anthology_sqlite import AnthologySqlite

class BaseTask(object):
    @classmethod
    def run(cls):
        sqlite = AnthologySqlite()
        sqlite.create_tables()
        sqlite.sqlite_shell()


        # downloader = PaperDownloader()
        #
        # filtered = papers.filter('title', 'commonsense') | papers.filter('abstract', 'commonsense')
        # downloader.multi_download(filtered, os.path.join(ACLConsts.LONG, 'commonsense_title_or_abstract'))


if __name__ == '__main__':
    BaseTask.run()

"""
@Desc:
"""
import os
from src.modules import Retriever
from src.modules.constants import ACLConsts
from src.modules.downloader import PaperDownloader
from src.modules.anthology_sqlite import AnthologySqlite
from src.modules.anthology_mysql import AnthologyMySQL

class BaseTask(object):
    @classmethod
    def run(cls):
        db = AnthologyMySQL(cache_enable=True)
        db.create_tables()
        db.load_data()  # 将数据爬取载入数据库中
        print(db.get_conferences())

        # downloader = PaperDownloader()
        #
        # filtered = papers.filter('title', 'commonsense') | papers.filter('abstract', 'commonsense')
        # downloader.multi_download(filtered, os.path.join(ACLConsts.LONG, 'commonsense_title_or_abstract'))


if __name__ == '__main__':
    BaseTask.run()

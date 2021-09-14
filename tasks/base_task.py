"""
@Desc:
@Reference:
https://github.com/lizhenggan/ABuilder
"""

import os
from ABuilder.ABuilder import ABuilder
from src.modules.downloader import PaperDownloader
from src.modules.papers import Paper, PaperList
from src.modules.anthology_mysql import AnthologyMySQL
from src.common.database_tools import MySQLTools

class BaseTask(object):
    @classmethod
    def load_data_to_db(cls):
        """
        将论文数据载入数据库
        """
        db = AnthologyMySQL(cache_enable=True)
        db.create_tables()
        db.load_data()  # 将数据爬取载入数据库中

    @classmethod
    def query_papers(cls, keyword: str):
        """
        检索论文
        """
        conf_contents = ['ACL', 'EMNLP', 'TACL', 'NAACL']
        years_limit = tuple(range(2016, 2022))
        data = ABuilder().table('paper')\
            .where({"year": ["in", years_limit]})\
            .where({"venue": ["in", conf_contents]}).query()
        papers = MySQLTools.list_to_papers(data)
        filtered = papers.containing_filter('title', keyword) | papers.containing_filter('abstract', keyword)
        return filtered

    @classmethod
    def download_papers(cls, papers: PaperList, keyword, conf_content):
        """
        检索论文
        """
        downloader = PaperDownloader()
        downloader.multi_download(papers, os.path.join(keyword, conf_content))

    @classmethod
    def run(cls):
        # cls.load_data_to_db()
        while True:
            keyword = input('type a keyword(blank will exit): ')
            if not keyword.strip():
                break
            papers = cls.query_papers(keyword)
            print(f'The size of papers: {papers.size}')
        # downloader = PaperDownloader()
        #
        # filtered = papers.filter('title', 'commonsense') | papers.filter('abstract', 'commonsense')
        # downloader.multi_download(filtered, os.path.join(ACLConsts.LONG, 'commonsense_title_or_abstract'))


if __name__ == '__main__':
    BaseTask.run()

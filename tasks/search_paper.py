"""
@Desc:
@Reference:
https://github.com/lizhenggan/ABuilder
pip install a-sqlbuilder
"""
import sys
sys.path.insert(0, '')    # 在tasks文件夹中可以直接运行程序

from typing import List
import os
from ABuilder.ABuilder import ABuilder
from src.modules.downloader import PaperDownloader
from src.common.file_tools import FileTools
from tasks.basic_task import BasicTask
from src.common.database_tools import MySQLTools



class MyTask(BasicTask):
    @classmethod
    def multi_keywords_query_papers(cls, keywords: List[str], conf_contents: list, years_limit: list):
        """
        检索论文
        """
        data = ABuilder().table('paper') \
            .where({"year": ["in", years_limit]}) \
            .where({"venue": ["in", conf_contents]}).query()
        papers = MySQLTools.list_to_papers(data)
        filtered = papers
        for keyword in keywords:
            filtered = filtered.containing_filter('title', keyword) | \
                filtered.containing_filter('abstract', keyword)
        return filtered

    @classmethod
    def run(cls):
        # Survey for text generation
        conf_contents_limit = ['ACL', 'EMNLP', 'NAACL', 'Findings']
        downloader = PaperDownloader()
        keywords = ['event', 'story generation']
        years_limit = list(range(2021, 2023))
        fields = ['title', 'abstract']
        papers = cls.multi_keywords_query_papers(keywords, conf_contents_limit, years_limit)
        downloader.logger.info(f'The size of papers: {papers.size}')

        group = papers.group('conf_content')

        print(papers)


if __name__ == '__main__':
    MyTask.run()

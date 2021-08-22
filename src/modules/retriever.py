"""
@Desc:
"""

import requests
from logging import DEBUG
from src.modules.constants import CACHE_DIR
from src.modules.papers import PaperList
from src.modules.statistics import Statistics as stats
from src.modules.statistics import Stat
from src.modules.logger import MyLogger
from src.modules.cache import LocalCache

class Retriever(object):
    _class_name = "ACL Anthology Retriever"

    def __init__(self, url, conference, year, conf_content, cache_enable=True):
        self.url = url
        self.conference = conference
        self.year = str(year)
        self.conf_content = str(conf_content)
        self.logger = MyLogger('retriever', DEBUG)
        self.cache_enable = cache_enable
        self.cache = LocalCache(f'{self.conf_content}_retriever') if self.cache_enable else None

        if self.cache_enable:
            self.cache.smart_load()
        self.papers = self._get_paper_list()
        self._collect_stats()

    @classmethod
    def acl(cls, year, content, cache_enable=True):
        return cls._make_conference("acl", year, content, cache_enable)

    @classmethod
    def _make_conference(cls, conference, year, conf_content, cache_enable=True):
        url = f"https://aclanthology.org/events/{conference}-{year}/#{conf_content}"
        return Retriever(url, conference, year, conf_content, cache_enable)

    def _get_paper_list(self):
        """
        :return:
        note:  PaperList cannot be serialized, because of containing logging
        """
        if self.cache and self.conf_content in self.cache:
            papar_list = self.cache[self.conf_content]
            instance = PaperList(papers=papar_list, logger=self.logger)
        else:
            response = requests.get(self.url)
            instance = PaperList.init_from_response(self.conf_content, self.year, response.content, self.logger)
            if self.cache_enable:
                self.cache[self.conf_content] = instance.papers
                self.cache.store(local_dir=CACHE_DIR)
        return instance

    def _collect_stats(self):
        stats.add(Stat(f'{self.conf_content}').add_attr('papers', len(self.papers)))
        self.logger.info(stats.repr())

    def __repr__(self):
        repr_content = f"========== {self._class_name}: ============\n"
        for attribute_name, attribute_value in self.__dict__.items():
            repr_content += f"{str(attribute_name).upper()} : {attribute_value}\n"
        return repr_content

"""
@Desc:
"""

import requests
from logging import DEBUG
from src.modules.constants import CACHE_DIR
from src.modules.conferences import Anthology
from src.modules.papers import PaperList
from src.modules.statistics import Statistics as stats
from src.modules.statistics import Stat
from src.modules.logger import MyLogger
from src.modules.cache import LocalCache


class Retriever(object):
    _class_name = "ACL Anthology Retriever"

    def __init__(self, cache_enable=True, cache_dir=CACHE_DIR, log_path=''):
        self.homepage_url = "https://aclanthology.org"
        self.logger = MyLogger('retriever', DEBUG, log_path)
        self.cache_enable = cache_enable
        if self.cache_enable:
            self.cache = LocalCache('retriever', cache_dir, self.logger)
            self.cache.smart_load()
        else:
            self.cache = None

    def load_anthology(self):
        """
        :return:
        note:  Anthology cannot be serialized, because of containing logging
        """
        _cache_key = 'anthology'
        if self.cache and _cache_key in self.cache:
            conf_dict = self.cache[_cache_key]
            anthology = Anthology(confs=conf_dict, logger=self.logger)
        else:
            anthology = Anthology(confs={}, logger=self.logger)
            anthology.parse_htmls()
            if self.cache_enable:
                self.cache[_cache_key] = anthology.confs
                self.cache.store()
        return anthology

    def get_paper_list_from_volumes(self, conf, conf_content, year, url):
        return PaperList.init_from_volumes_response(conf, conf_content, year, url, self.logger)

    def _get_paper_list(self, conf, year, conf_content):
        """
        :return:
        note:  PaperList cannot be serialized, because of containing logging
        """
        if self.cache and conf_content in self.cache:
            paper_list = self.cache[conf_content]
            paper_list_obj = PaperList(papers=paper_list, logger=self.logger)
        else:
            target_url = f"{self.homepage_url}/events/{conf}-{year}/#{conf_content}"
            response = requests.get(target_url)
            paper_list_obj = PaperList.init_from_events_response(conf, conf_content, year, response.content,
                                                                 self.logger)
            if self.cache_enable:
                self.cache[conf_content] = paper_list_obj.papers
                self.cache.store()
        return paper_list_obj

    def _collect_stats(self, conf_content, papers):
        stats.add(Stat(f'{conf_content}').add_attr('papers', len(papers)))
        self.logger.info(stats.repr())

    @classmethod
    def acl(cls, year, conf_content, cache_enable=True) -> PaperList:
        retriever = Retriever(cache_enable=cache_enable)
        papers = retriever._get_paper_list("acl", year, conf_content)
        retriever._collect_stats(conf_content, papers)
        return papers

    @classmethod
    def naacl(cls, year, conf_content, cache_enable=True) -> PaperList:
        retriever = Retriever(cache_enable=cache_enable)
        papers = retriever._get_paper_list("naacl", year, conf_content)
        retriever._collect_stats(conf_content, papers)
        return papers

    @classmethod
    def emnlp(cls, year, conf_content, cache_enable=True) -> PaperList:
        retriever = Retriever(cache_enable=cache_enable)
        papers = retriever._get_paper_list("emnlp", year, conf_content)
        retriever._collect_stats(conf_content, papers)
        return papers

    def __repr__(self):
        repr_content = f"========== {self._class_name}: ============\n"
        for attribute_name, attribute_value in self.__dict__.items():
            repr_content += f"{str(attribute_name).upper()} : {attribute_value}\n"
        return repr_content

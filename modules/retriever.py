"""
@Author: Travis Tang
@Date: 2021.8.17
@Desc:
"""

import requests
from bs4 import BeautifulSoup as Soup
from .constants import CachesConsts
from .papers import PaperList

class Retriever(object):
    _class_name = "ACL Anthology Retriever"

    def __init__(self, url, conference, year, conf_content):
        self.url = url
        self.conference = conference
        self.year = str(year)
        self.conf_content = str(conf_content)
        self.caches = dict()
        self.paper_list = self._get_paper_list()

    @classmethod
    def acl(cls, year, content):
        return cls._make_conference("acl", year, content)

    @classmethod
    def _make_conference(cls, conference, year, conf_content):
        url = f"https://aclanthology.org/events/{conference}-{year}/#{conf_content}"
        return Retriever(url, conference, year, conf_content)

    def _get_paper_list(self):
        if not self.caches.get(CachesConsts.ROOT, None):
            self.caches[CachesConsts.ROOT] = requests.get(self.url)
        response = self.caches[CachesConsts.ROOT]
        if not response.ok:
            return PaperList()
        else:
            return PaperList.init_from_response(self.conf_content, self.year, response.content)


    def __repr__(self):
        repr_content = f"========== {self._class_name}: ============\n"
        for attribute_name, attribute_value in self.__dict__.items():
            repr_content += f"{str(attribute_name).upper()} : {attribute_value}\n"
        return repr_content












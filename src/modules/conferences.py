"""
@Desc:
"""
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup as Soup
from .logger import MyLogger
from src.common.string_tools import StringTools


class Conference(object):
    def __init__(self, name, label):
        self.name = name
        self.label = label  # ACL Events / Non-ACL Events
        self.conf_contents = []
        self.tuples = []

    def __repr__(self):
        repr_content = f'\nConference "{self.name}":\n'
        for attribute_name, attribute_value in self.__dict__.items():
            repr_content += f"{self.tuples}"
        return repr_content


class Anthology(object):
    def __init__(self, confs=[], logger=None):
        self.name = "Anthology"
        self.homepage_url = "https://aclanthology.org/"
        self.confs = confs
        self.logger = logger

    @property
    def size(self):
        return len(self.confs)

    def parse_htmls(self):
        response = requests.get(self.homepage_url)
        page = Soup(response.content, "html.parser")
        # segment of papers
        events = page.find_all("tbody")
        acl_events = events[0]
        non_ack_events = events[1]
        # TODO: parse htmls
        pass
        # # get info from infobox ===========
        # # the first is not a paper.
        # infobox_set = core.find_all("p", {"class": "d-sm-flex align-items-stretch"})[1:]
        # for one in tqdm(infobox_set, desc='parsing infobox_set'):
        #     infobox = one.find_all("span", {"class", "d-block"})[1]
        #     title_with_href = infobox.find("a", {"class": "align-middle"})
        #     title = title_with_href.get_text().strip()
        #     href = title_with_href.get("href")
        #     url = f'https://aclanthology.org{href[:-1]}.pdf'
        #     # authors
        #     authors = []
        #     for author in infobox.find_all("a"):
        #         authors.append(author.get_text().strip())
        #     _paper_list.papers.append(Paper(title, year, url, authors))
        #
        # # get info from abstract ===========
        # abstract_set = core.find_all("div", {"class", "card-body p-3 small"})
        # if len(abstract_set) != len(_paper_list):
        #     raise ValueError
        # for one, paper in tqdm(zip(abstract_set, _paper_list), desc='parsing abstract_set'):
        #     abstract = one.get_text().strip()
        #     paper.abstract = abstract

    def add_logger(self, logger: MyLogger):
        self.logger = logger

    def items(self):
        return self.confs

    def __iter__(self):
        for conf in self.confs:
            yield conf

    def __call__(self, *args, **kwargs):
        return self.confs

    def __repr__(self):
        repr_content = f'\n'
        for one in self.confs:
            repr_content += str(one)
        return repr_content

    def __len__(self):
        return len(self.confs)

"""
@Desc:
"""
import requests
import json
import itertools
from tqdm import tqdm
from bs4 import BeautifulSoup as Soup
from .logger import MyLogger
from .constants import ConfConsts
from src.common.serialization_tools import MyEncoder


class Conference(object):
    def __init__(self, name, label, link):
        self.name = name
        self.label = label  # ACL Events / Non-ACL Events
        self.link = link
        self.conf_contents = {}

    @property
    def size(self):
        return sum([len(contents) for contents in self.conf_contents.values()])

    def __iter__(self):
        for content in self.conf_contents:
            yield content

    def __call__(self, *args, **kwargs):
        return self.conf_contents

    def __repr__(self):
        return f'Conference {self.name}:\n' + json.dumps(self.conf_contents, indent=4, cls=MyEncoder)

    def __str__(self):
        return self.__repr__()


class ConfContent(object):
    def __init__(self, name, full_name, year, link, volume_size):
        self.name = name
        self.full_name = full_name
        self.year = year
        self.link = link
        self.volume_size = volume_size

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.__repr__()


class Anthology(object):
    def __init__(self, confs=None, logger=None):
        if confs is None:
            confs = {ConfConsts.ACL_EVENTS: [], ConfConsts.NON_ACL_EVENTS: []}
        elif not isinstance(confs, dict):
            raise ValueError("confs should be dict.")
        self.name = "Anthology"
        self.homepage_url = "https://aclanthology.org"
        self.confs = confs
        self.logger = logger

        # initialization
        self.init_confs()

    def init_confs(self):
        if ConfConsts.ACL_EVENTS not in self.confs:
            self.confs[ConfConsts.ACL_EVENTS] = []
        if ConfConsts.NON_ACL_EVENTS not in self.confs:
            self.confs[ConfConsts.NON_ACL_EVENTS] = []

    @property
    def size(self):
        return sum([len(conferences) for conferences in self.confs.values()])

    def parse_htmls(self):
        self.fill_with_conf_infos()
        self.fill_with_conf_contents()

    def fill_with_conf_infos(self):
        response = requests.get(self.homepage_url)
        acl_homepage = Soup(response.content, "html.parser")
        events = acl_homepage.find_all("tbody")
        acl_events = events[0]
        non_ack_events = events[1]

        # acl events
        rows = acl_events.find_all("tr", {"class", "text-center"})
        for row in tqdm(rows, desc='parsing acl events'):
            conf = row.find("th")
            conf_name = conf.get_text().strip()
            # SIGs are not conferences
            if conf_name == "SIGs":
                continue
            conf_link = f'https://aclanthology.org/{conf.find("a").get("href")}'
            self.confs[ConfConsts.ACL_EVENTS].append(Conference(conf_name, ConfConsts.ACL_EVENTS, conf_link))

        # non-acl events
        rows = non_ack_events.find_all("tr", {"class", "text-center"})
        for row in tqdm(rows, desc='parsing non-acl events'):
            conf = row.find("th")
            conf_name = conf.get_text().strip()
            conf_link = f'{self.homepage_url}{conf.find("a").get("href")}'
            self.confs[ConfConsts.NON_ACL_EVENTS].append(Conference(conf_name, ConfConsts.NON_ACL_EVENTS, conf_link))

    def fill_with_conf_contents(self):
        for conf in tqdm(itertools.chain(*self.confs.values()), total=self.size, desc='parsing all conf_contents'):
            response = requests.get(conf.link)
            conf_html = Soup(response.content, "html.parser")
            for year_conf_html in conf_html.find_all("div", {"class", "row"}):
                year = year_conf_html.find("h4").get_text()  # year
                conf.conf_contents[year] = []
                # traverse contents
                for content in year_conf_html.find_all("li"):
                    a = content.find("a")
                    href = a.get("href")
                    name = href.split("/")[2]
                    full_name = a.get_text().strip()
                    link = f'{self.homepage_url}{href}'
                    #   is blank for html.
                    volume_size = int(content.find("span").get_text().split(" ")[0].strip())
                    conf.conf_contents[year].append(ConfContent(name, full_name, year, link, volume_size))

    def add_logger(self, logger: MyLogger):
        self.logger = logger

    def items(self):
        return self.confs.items()

    def __iter__(self):
        for conf in self.confs:
            yield conf

    def __call__(self, *args, **kwargs):
        return self.confs

    def __repr__(self):
        return 'Anthology:\n' + json.dumps(self.confs, indent=4, cls=MyEncoder)

    def __str__(self):
        return self.__repr__()

    def __len__(self):
        return sum([len(one) for one in self.confs.values()])

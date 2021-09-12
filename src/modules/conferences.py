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
from src.common.string_tools import StringTools


class Conference(object):
    def __init__(self, name, label, link):
        self.name = name
        self.label = label  # ACL Events / Non-ACL Events
        self.link = link
        self.conf_contents = {}

    def __repr__(self):
        return f'Conference {self.name}:/n' + json.dumps(self.conf_contents, indent=4)


class ConfContents(object):
    def __init__(self, name, link):
        self.name = name
        self.link = link

    def __repr__(self):
        return self.name


class Anthology(object):
    def __init__(self, confs=None, logger=None):
        if confs is None:
            confs = {ConfConsts.ACL_EVENTS: [], ConfConsts.NON_ACL_EVENTS: []}
        elif not isinstance(confs, dict):
            raise ValueError("confs should be dict.")
        self.name = "Anthology"
        self.homepage_url = "https://aclanthology.org/"
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
        return len(self.confs)

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
        for row in acl_events.find_all("tr", {"class", "text-center"}):
            conf = row.find("th")
            conf_name = conf.get_text().strip()
            conf_link = f'https://aclanthology.org/{conf.get("href")}'
            self.confs[ConfConsts.ACL_EVENTS].append(Conference(conf_name, ConfConsts.ACL_EVENTS, conf_link))

        # non-acl events
        for row in non_ack_events.find_all("text center"):
            conf = row.find("th")
            conf_name = conf.get_text().strip()
            conf_link = f'https://aclanthology.org/{conf.get("href")}'
            self.confs[ConfConsts.NON_ACL_EVENTS].append(Conference(conf_name, ConfConsts.NON_ACL_EVENTS, conf_link))

    def fill_with_conf_contents(self):
        # for conf in itertools.chain(*self.confs.values()):
        #     response = requests.get(conf.link)
        #     conf_html = Soup(response.content, "html.parser")
        pass

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
        repr_content = f'\n'
        repr_content += json.dumps(self.confs, indent=4)
        return repr_content

    def __len__(self):
        return sum([len(one) for one in self.confs.values()])

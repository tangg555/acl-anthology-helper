"""
@Desc:
"""
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup as Soup
from .logger import MyLogger
from src.common.string_tools import StringTools


class Paper(object):
    def __init__(self, title, year, url, authors=[], abstrat="", conf_content="", venue=""):
        self.title = title
        self.year = year
        self.url = url
        self.authors = authors
        self.abstract = abstrat
        self.conf_content = conf_content
        self.venue = venue
        self.reader_desc = ''  # I can add some descriptions to this paper

    def add_desc(self, desc: str):
        self.reader_desc += desc + '||\n'

    def __repr__(self):
        repr_content = f'\nPaper "{self.title}":\n'
        for attribute_name, attribute_value in self.__dict__.items():
            if attribute_name == "title":
                continue
            repr_content += f"{attribute_name} : {attribute_value};\t"
        return repr_content


class PaperList(object):
    def __init__(self, papers=[], logger=None):
        self.name = "PaperList"
        self.papers = papers
        self.logger = logger

    @property
    def size(self):
        return len(self.papers)

    @classmethod
    def init_from_volumes_response(cls, conf, conf_content, year, url, logger=None):
        """
        e.g. https://aclanthology.org/volumes/2021.acl-long/
        """
        _paper_list = PaperList([], logger)
        response = requests.get(url)
        page = Soup(response.content, "html.parser")

        # get info from infobox ===========
        # the first is not a paper.
        infobox_set = page.find_all("p", {"class": "d-sm-flex align-items-stretch"})[1:]
        for one in infobox_set:
            infobox = one.find_all("span", {"class", "d-block"})[1]
            title_with_href = infobox.find("a", {"class": "align-middle"})
            title = title_with_href.get_text().strip()
            href = title_with_href.get("href")
            url = f'https://aclanthology.org{href[:-1]}.pdf'
            # authors
            authors = []
            skip_first = True
            for author in infobox.find_all("a"):
                if skip_first:
                    skip_first = False
                    continue
                authors.append(author.get_text().strip())
            _paper_list.papers.append(Paper(title, year, url, authors, conf_content=conf_content, venue=conf))

        # get info from abstract ===========
        abstract_set = page.find_all("div", {"class", "card-body p-3 small"})
        # 如果数量对不上的话只能跳过，不载入abstract
        if len(abstract_set) == len(_paper_list):
            for one, paper in zip(abstract_set, _paper_list):
                abstract = one.get_text().strip()
                paper.abstract = abstract
        return _paper_list

    @classmethod
    def init_from_events_response(cls, conf, conf_content, year, r_content, logger=None):
        """
        e.g. https://aclanthology.org/events/acl-2021/
        """
        _paper_list = PaperList([], logger)
        page = Soup(r_content, "html.parser")
        # segment of papers
        core = page.find("div", {"id": conf_content})

        # get info from infobox ===========
        # the first is not a paper.
        infobox_set = core.find_all("p", {"class": "d-sm-flex align-items-stretch"})[1:]
        for one in tqdm(infobox_set, desc='parsing infobox_set'):
            infobox = one.find_all("span", {"class", "d-block"})[1]
            title_with_href = infobox.find("a", {"class": "align-middle"})
            title = title_with_href.get_text().strip()
            href = title_with_href.get("href")
            url = f'https://aclanthology.org{href[:-1]}.pdf'
            # authors
            authors = []
            skip_first = True
            for author in infobox.find_all("a"):
                if skip_first:
                    skip_first = False
                    continue
                authors.append(author.get_text().strip())
            _paper_list.papers.append(Paper(title, year, url, authors, conf_content=conf_content, venue=conf))

        # get info from abstract ===========
        abstract_set = core.find_all("div", {"class", "card-body p-3 small"})
        # 如果数量对不上的话只能跳过，不载入abstract
        if len(abstract_set) == len(_paper_list):
            for one, paper in tqdm(zip(abstract_set, _paper_list), desc='parsing abstract_set'):
                abstract = one.get_text().strip()
                paper.abstract = abstract

        return _paper_list

    def add_logger(self, logger: MyLogger):
        self.logger = logger

    '''
    ============================ filters ============================
    '''

    def containing_filter(self, attr: str, keyword: str):
        filtered = []
        for paper in self.papers:
            if StringTools.contain(eval(f'paper.{attr}'), keyword):
                paper.add_desc(f'filtered by containing "{keyword}" in {attr}')
                filtered.append(paper)
        if isinstance(self.logger, MyLogger):
            self.logger.info(
                f'filtered by containing "{keyword}" in {attr} for {len(self.papers)} papers,'
                f' remaining {len(filtered)}')
        return PaperList(filtered)

    def or_containing_filter(self, attr: str, keywords: list):
        filtered = []
        for paper in self.papers:
            if StringTools.multi_or_contain(eval(f'paper.{attr}'), keywords):
                paper.add_desc(f'filtered by containing [{" or ".join(keywords)}] in {attr}')
                filtered.append(paper)
        if isinstance(self.logger, MyLogger):
            self.logger.info(
                f'filtered by containing [{" or ".join(keywords)}] in {attr} for {len(self.papers)} papers,'
                f' remaining {len(filtered)}')
        return PaperList(filtered)

    def and_containing_filter(self, attr: str, keywords: list):
        filtered = []
        for paper in self.papers:
            if StringTools.multi_and_contain(eval(f'paper.{attr}'), keywords):
                paper.add_desc(f'filtered by containing [{" and ".join(keywords)}] in {attr}')
                filtered.append(paper)
        if isinstance(self.logger, MyLogger):
            self.logger.info(
                f'filtered by containing [{" and ".join(keywords)}] in {attr} for {len(self.papers)} papers,'
                f' remaining {len(filtered)}')
        return PaperList(filtered)

    def group(self, attr: str) -> dict:
        group_dict = {}
        for paper in self.papers:
            key = eval(f'paper.{attr}')
            if key not in group_dict:
                group_dict[key] = PaperList(papers=[])
            group_dict[key].papers.append(paper)
        return group_dict

    def items(self):
        return self.papers

    def __and__(self, other):
        new = PaperList(papers=list(set(self.papers) & set(other.papers)), logger=self.logger)
        return new

    def __or__(self, other):
        new = PaperList(papers=list(set(self.papers) | set(other.papers)), logger=self.logger)
        return new

    def __iter__(self):
        for paper in self.papers:
            yield paper

    def __call__(self, *args, **kwargs):
        return self.papers

    def __repr__(self):
        repr_content = f'\n'
        for one in self.papers:
            repr_content += str(one)
        return repr_content

    def __len__(self):
        return len(self.papers)

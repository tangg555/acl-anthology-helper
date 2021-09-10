"""
@Desc:
"""
from tqdm import tqdm
from bs4 import BeautifulSoup as Soup
from .logger import MyLogger
from src.common.string_tools import StringTools


class Conference(object):
    def __init__(self, name):
        self.name = name
        self.conf_contents = []
        self.tuples = []

    def __repr__(self):
        repr_content = f'\nConference "{self.name}":\n'
        for attribute_name, attribute_value in self.__dict__.items():
            repr_content += f"{self.tuples}"
        return repr_content

class Anthology(object):
    def __init__(self, papers=[], logger=None):
        self.name = "PaperList"
        self.papers = papers
        self.logger = logger

    @property
    def size(self):
        return len(self.papers)

    @classmethod
    def init_from_response(cls, conf_content, year, r_content, logger=None):
        _paper_list = PaperList([], logger)
        page = Soup(r_content, "html.parser")
        # segment of papers
        core = page.find("div", {"id": conf_content})

        # get info from infobox ===========
        # the first is not a paper.
        infobox_set = core.find_all("p", {"class": "d-sm-flex align-items-stretch"})[1:]
        for one in tqdm(infobox_set, desc='parsing infobox_set'):
            infobox = one.find_all("span", {"class", "d-block"})[1]
            title_with_href= infobox.find("a", {"class": "align-middle"})
            title = title_with_href.get_text().strip()
            href = title_with_href.get("href")
            url = f'https://aclanthology.org{href[:-1]}.pdf'
            #authors
            authors = []
            for author in infobox.find_all("a"):
                authors.append(author.get_text().strip())
            _paper_list.papers.append(Paper(title, year, url, authors))

        # get info from abstract ===========
        abstract_set = core.find_all("div", {"class", "card-body p-3 small"})
        if len(abstract_set) != len(_paper_list):
            raise ValueError
        for one, paper in tqdm(zip(abstract_set,_paper_list ), desc='parsing abstract_set'):
            abstract = one.get_text().strip()
            paper.abstract = abstract

        return _paper_list

    def add_logger(self, logger: MyLogger):
        self.logger = logger

    def filter(self, key: str, val: str):
        filtered = []
        for paper in self.papers:
            if StringTools.contain(eval(f'paper.{key}'), val):
                paper.add_desc(f'filtered by containing "{val}" in {key}')
                filtered.append(paper)
        if isinstance(self.logger, MyLogger):
            self.logger.info(f'filtered by containing "{val}" in {key} for {len(self.papers)}, remaining {len(filtered)}')
        return PaperList(filtered)

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


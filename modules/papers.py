"""
@Author: Travis Tang
@Date: 2021.8.18
@Desc:
"""
from bs4 import BeautifulSoup as Soup

class Paper(object):
    def __init__(self, title, year, url,  authors=[], abstrat=""):
        self.title = title
        self.year = year
        self.url = url
        self.authors = authors
        self.abstract = abstrat

    def __repr__(self):
        repr_content = f'\nPaper "{self.title}":\n'
        for attribute_name, attribute_value in self.__dict__.items():
            if attribute_name == "title":
                continue
            repr_content += f"{attribute_name} : {attribute_value};\t"
        return repr_content


class PaperList(object):
    def __init__(self):
        self.papers = []

    @classmethod
    def init_from_response(cls, conf_content, year, r_content):
        _paper_list = PaperList()
        page = Soup(r_content, "html.parser")
        # segment of papers
        papers = page.find("div", {"id": conf_content})
        for one in papers.find_all("p", {"class": "d-sm-flex align-items-stretch"}):
            infobox = one.find_all("span", {"class", "d-block"})[1]
            title_with_href= infobox.find("a", {"class": "align-middle"})
            title = title_with_href.get_text().strip()
            href = title_with_href.get("href")
            url = f'https://aclanthology.org/{href}.pdf'
            #authors
            authors = []
            for author in infobox.find_all("a"):
                authors.append(author.get_text().strip())
            _paper_list.papers.append(Paper(title, year, url, authors))
        return _paper_list

    def __repr__(self):
        repr_content = f'\n'
        for one in self.papers:
            repr_content += str(one)
        return repr_content

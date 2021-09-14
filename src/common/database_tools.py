from src.modules.papers import Paper, PaperList

class MySQLTools(object):
    @classmethod
    def dict_to_paper(cls, result: dict):
        paper = Paper(
            title=result['title'],
            year=result['year'],
            url=result['url'],
            authors=result['authors'].split(', '),
            abstrat=result['abstract'],
            conf_content=result['conf_content'],
            venue=result['venue']
        )
        return paper

    @classmethod
    def list_to_papers(cls, result: list):
        paper_list = []
        for one in result:
            paper_list.append(cls.dict_to_paper(one))
        return PaperList(papers=paper_list)

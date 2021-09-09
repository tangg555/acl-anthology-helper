import sys
import os
from pathlib import Path
from .models import Conference, Paper

# PACKAGE_DIR = Path(__file__).resolve().parent.parent.parent.parent
# sys.path.insert(0, PACKAGE_DIR)
# sys.path.insert(0, os.path.join(PACKAGE_DIR, 'src'))

from src.modules.retriever import Retriever

def load_papers_to_db(conference, year, conf_content):
    conf = Retriever.make_conference(conference, year, conf_content, cache_enable=True)  # use local cache
    Conference.objects.get_or_create(name=conference, year=year)
    for paper in conf.papers:
        Paper.objects.get_or_create(title=paper.title, conf=conference, year=paper.year, conf_content=conf_content,
                                    url=paper.url, authors=paper.authors,
                                    abstract=paper.abstract, reader_desc=paper.reader_desc)
    return Paper.objects.filter(conf=conference).filter(year=year).filter(conf_content=conf_content)


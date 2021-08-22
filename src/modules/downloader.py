"""
@reference:
python下载文件的三种方法
https://www.jianshu.com/p/e137b03a1cd2
"""

from logging import DEBUG
import os
import requests
from tqdm import tqdm
from src.modules.logger import MyLogger
from src.modules.papers import Paper, PaperList
from src.common.string_tools import String


class Downloader(object):
    def set_downlard_dir(self, path):
        pass

    def download(self, obj, prefix_dir, with_info=False):
        pass

    def multi_download(self, objs, prefix_dir, with_info=False):
        pass


class PaperDownloader(Downloader):
    def __init__(self, download_dir='./download', logger=None):
        self._download_dir = download_dir
        self._logger = logger if logger else MyLogger('downloader', DEBUG)

    def download(self, paper: Paper, prefix_path, with_info=False):
        prefix = os.path.join(self._download_dir, prefix_path)
        if not os.path.exists(prefix):
            os.makedirs(prefix)
        fpath = os.path.join(prefix, f'{String.fileNameNorm(paper.title)}.pdf')
        r = requests.get(paper.url)
        with open(fpath, "wb") as f:
            f.write(r.content)
        if with_info:
            self._logger.info(f'paper downloaded at {fpath}')

    def multi_download(self, papers: PaperList, prefix_path, with_info=False):
        """
        :param papers:
        :param prefix_path:
        :param with_info:
        :return:
        without multiprocessing.
        """
        self._logger.info(f'Papers multi_download(without multi-processing) starts, papers: {papers.size}')
        for paper in tqdm(papers, desc=f"multi downloading", total=papers.size):
            self.download(paper, prefix_path)
        self._logger.info('All subprocesses done.')

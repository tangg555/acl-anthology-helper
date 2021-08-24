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
from src.common.string_tools import StringTools
from src.common.file_tools import FileTools


class Downloader(object):
    def __init__(self, download_dir='./download', logger=None):
        self._download_dir = download_dir
        self._logger = logger if logger else MyLogger('downloader', DEBUG)

    def set_downlard_dir(self, path):
        pass

    def download(self, obj, prefix_dir, with_info=False):
        pass

    def multi_download(self, objs, prefix_dir, with_info=False):
        pass


class PaperDownloader(Downloader):
    def set_downlard_dir(self, download_dir: str):
        if not os.path.isdir(download_dir):
            raise FileExistsError(f'The input directory -{download_dir}- is invalid.')
        self._download_dir = download_dir

    def download(self, paper: Paper, prefix_dir, with_info=False):
        prefix = os.path.join(self._download_dir, prefix_dir)
        if not os.path.exists(prefix):
            os.makedirs(prefix)
        fpath = os.path.join(prefix, f'{StringTools.fileNameNorm(paper.title)}.pdf')
        r = requests.get(paper.url)
        with open(fpath, "wb") as f:
            f.write(r.content)
        if with_info:
            self._logger.info(f'paper downloaded at {fpath}')

    def multi_download(self, papers: PaperList, prefix_dir, with_info=False):
        """
        :param papers:
        :param prefix_path:
        :param with_info:
        :return:
        without multiprocessing.
        """
        self._logger.info(f'Papers multi_download(without multi-processing) starts, papers: {papers.size}')
        success = 0
        fails = []
        for paper in tqdm(papers, desc=f"multi downloading", total=papers.size):
            try:
                self.download(paper, prefix_dir)
                success += 1
            except Exception as e:
                self._logger.warning(f'{paper} download failed, the exception is :{e}')
                fails.append(paper)
        self._logger.info('All subprocesses done.')
        prefix = os.path.join(self._download_dir, prefix_dir)
        FileTools.info_to_file(papers, os.path.join(prefix, 'papers_info.txt'))
        FileTools.info_to_file(f'{success} downloaded, total: {papers.size}\nfailed papers:\n{fails}',
                               os.path.join(prefix, 'download_info.txt'))

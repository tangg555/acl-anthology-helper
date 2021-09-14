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
        self.download_dir = download_dir
        self.logger = logger if logger else MyLogger('downloader', DEBUG)

    def set_downlard_dir(self, path):
        pass

    def download(self, obj, prefix_dir, verbose=False):
        pass

    def multi_download(self, objs, prefix_dir, verbose=False):
        pass


class PaperDownloader(Downloader):
    def set_downlard_dir(self, download_dir: str):
        if not os.path.isdir(download_dir):
            raise FileExistsError(f'The input directory -{download_dir}- is invalid.')
        self.download_dir = download_dir

    def download(self, paper: Paper, prefix_dir, verbose=False):
        prefix = os.path.join(self.download_dir, prefix_dir)
        if not os.path.exists(prefix):
            os.makedirs(prefix)
        fpath = os.path.join(prefix, f'{StringTools.filename_norm(paper.title)}.pdf')
        r = requests.get(paper.url)
        with open(fpath, "wb") as f:
            f.write(r.content)
        if verbose:
            self.logger.info(f'paper downloaded at {fpath}')

    def multi_download(self, papers: PaperList, prefix_dir, verbose=False):
        """
        :param papers:
        :param prefix_path:
        :param verbose:
        :return:
        without multiprocessing.
        """
        self.logger.info(f'Papers multi_download(without multi-processing) starts, papers: {papers.size}')
        success = 0
        fails = []
        for paper in tqdm(papers, desc=f"multi downloading", total=papers.size):
            try:
                self.download(paper, prefix_dir)
                success += 1
            except Exception as e:
                self.logger.warning(f'{paper} download failed, the exception is :{e}')
                fails.append(paper)
        self.logger.info('All subprocesses done.')
        prefix = os.path.join(self.download_dir, prefix_dir)
        FileTools.info_to_file(papers, os.path.join(prefix, 'papers_info.txt'))
        FileTools.info_to_file(f'{success} downloaded, total: {papers.size}\nfailed papers:\n{fails}',
                               os.path.join(prefix, 'download_info.txt'))

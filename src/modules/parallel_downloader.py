"""
@reference:
Python 3 爬虫｜第4章：多进程并发下载
https://madmalls.com/blog/post/multi-process-for-python3/

并行有诸多限制:
1.设计并行下载类的时候不能引入带锁的东西（如logging）
2.如果子任务报异常需要设计处理handler
"""
from logging import Logger, DEBUG
import os
import requests
from src.modules.logger import MyLogger
from src.modules.papers import Paper, PaperList
from src.common.string_tools import StringTools
from src.common.file_tools import FileTools
from multiprocessing import Pool


class PaperDownloader(object):
    def __init__(self, download_dir='./download', logger=None):
        self._download_dir = download_dir
        self._logger = logger if logger else MyLogger('downloader', DEBUG)

    def set_downlard_dir(self, download_dir: str):
        if not os.path.isdir(download_dir):
            raise FileExistsError(f'The input directory -{download_dir}- is invalid.')
        self._download_dir = download_dir

    @staticmethod
    def download(paper: Paper, download_dir, prefix_path):
        try:
            prefix = os.path.join(download_dir, prefix_path)
            os.makedirs(prefix, exist_ok=True)
            fpath = os.path.join(prefix, f'{StringTools.fileNameNorm(paper.title)}.pdf')
            r = requests.get(paper.url)
            with open(fpath, "wb") as f:
                f.write(r.content)
        except Exception as e:
            print(f'{paper} download failed, the exception is :{e}')

    def multi_download(self, papers: PaperList, prefix_dir):
        cpu_cores = os.cpu_count()  # number of parallel
        download_dir = self._download_dir
        self._logger.info(
            f'Papers multi_download(parallel) starts, cpus: {cpu_cores},'
            f' download_dir: {os.path.abspath(download_dir)},'
            f' papers: {papers.size}')
        params = []
        for paper in papers.items():
            params.append((paper, download_dir, prefix_dir))
        with Pool(cpu_cores) as process:
            process.starmap(self.download, params)
        self._logger.info('All subprocesses done.')
        prefix = os.path.join(self._download_dir, prefix_dir)
        FileTools.info_to_file(papers, os.path.join(prefix, 'papers_info.txt'))

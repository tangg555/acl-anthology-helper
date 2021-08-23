"""
@reference:
Python 3 爬虫｜第4章：多进程并发下载
https://madmalls.com/blog/post/multi-process-for-python3/

并行有诸多限制:
1.设计并行下载类的时候不能引入带锁的东西（如logging）
2.如果子任务报异常需要设计处理handler
"""

import os
import wget
from multiprocessing import Pool
from tqdm import tqdm
from src.modules.logger import MyLogger
from src.modules.papers import Paper, PaperList
from src.common.string_tools import StringTools

class ParallelDownloader(object):
    def set_downlard_dir(self, path):
        pass

    def multi_download(self, objs, prefix_dir, with_info=False):
        pass

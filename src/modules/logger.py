"""
@Desc:
Rrinting log to both screen and files.
@Reference:
https://xnathan.com/2017/03/09/logging-output-to-screen-and-file/
"""

import logging
import os
from logging import Logger
from logging import NOTSET

class MyLogger(Logger):
    def __init__(self, name, level=NOTSET, log_path=''):
        super(MyLogger, self).__init__(name, level)
        self.log_path = log_path if log_path else f'log/{name}_log.txt'
        self._init()

    def _init(self):
        warns = ''

        self.setLevel(self.level)
        formatter = logging.Formatter(
            "%(asctime)s %(pathname)s %(filename)s %(funcName)s %(lineno)s %(levelname)s - %(message)s",
            "%Y-%m-%d %H:%M:%S")

        # 使用FileHandler输出到文件
        if not os.path.exists(self.log_path):
            os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
            warns = f'{self.log_path} did not exist, and has been created now.'
        fh = logging.FileHandler(f'{self.log_path}')
        fh.setLevel(self.level)
        fh.setFormatter(formatter)

        # 使用StreamHandler输出到屏幕
        ch = logging.StreamHandler()
        ch.setLevel(self.level)
        ch.setFormatter(formatter)

        # 添加两个Handler
        self.addHandler(ch)
        self.addHandler(fh)

        # output warning
        if warns:
            self.warning(warns)
        self.info(f'MyLogger instance {self.name} has been set. level: {self.level}, log_path: {self.log_path}')












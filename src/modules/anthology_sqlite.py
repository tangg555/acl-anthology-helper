"""
@Reference"
使用SQLite
https://www.liaoxuefeng.com/wiki/1016959663602400/1017801751919456
Python自带的Sqlite支持shell命令行交互模式吗？
https://www.zhihu.com/question/62897833/answer/559922232
"""
import os
import sqlite3
from logging import DEBUG
from src.modules.retriever import Retriever
from src.modules.logger import MyLogger
from src.modules.constants import DBConsts


class AnthologySqlite(object):
    _class_name = "Anthology Sqlite"

    def __init__(self, cache_enable=True, log_path='', db_dir='./database'):
        self.retriever = Retriever(cache_enable=cache_enable)
        self.anthology = self.retriever.load_anthology()  # use local cache
        self.logger = MyLogger(self._class_name, DEBUG, log_path)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
            self.logger.warning(f'{db_dir} did not exist, and has been created now.')
        self.db_path = os.path.join(db_dir, DBConsts.ANTHOLOGY_DB)
        self.conn = None
        self.cursor = None

    def db_connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def db_disconnect(self):
        self.cursor.close()
        # 提交事务:
        self.conn.commit()
        # 关闭Connection:
        self.conn.close()

    def create_tables(self):
        self.db_connect()
        # conferences
        self.cursor.execute('''create table if not exists conference(id integer primary key auto_increment, 
                                conf_content char(20) not null, 
                                venue char(20), 
                                year integer, 
                                link char(50), 
                                volume_size integer);
                            ''')
        # papers
        self.cursor.execute('''create table if not exists paper(id int primary key auto_increment, 
                                title char(100) not null, 
                                year integer, 
                                url char(50), 
                                authors text, 
                                abstract text,
                                conf_content varchar(20));
                            ''')
        self.db_disconnect()

    def shell(self):
        self.db_connect()

        buffer = ""

        print("Enter your SQL commands to execute in sqlite3.")
        print("Enter a blank line to exit.")

        while True:
            line = input()
            if line == "":
                break
            buffer += line
            if sqlite3.complete_statement(buffer):
                try:
                    buffer = buffer.strip()
                    self.cursor.execute(buffer)

                    if buffer.lstrip().upper().startswith("SELECT"):
                        print(self.cursor.fetchall())
                except sqlite3.Error as e:
                    print("An error occurred:", e.args[0])
                buffer = ""

        self.db_disconnect()

    def __del__(self):
        if self.conn or self.cursor:
            self.db_disconnect()

"""
@Reference:
"""

import os
import itertools
import pymysql
from tqdm import tqdm
from logging import DEBUG
from src.modules.constants import CACHE_DIR
from src.modules.retriever import Retriever
from src.modules.logger import MyLogger
from src.modules.constants import DBConsts
from src.configuration.mysql_cfg import MySQLCFG
from src.modules.cache import LocalCache
from src.modules.papers import Paper
from src.modules.conferences import ConfContent


class AnthologyMySQL(object):
    _class_name = "Anthology MySQL"

    def __init__(self, cache_enable=True, cache_dir=CACHE_DIR, log_path='', db_dir='./database'):
        self.retriever = Retriever(cache_enable=cache_enable)
        self.anthology = self.retriever.load_anthology()  # use local cache
        self.logger = MyLogger(self._class_name, DEBUG, log_path)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
            self.logger.warning(f'{db_dir} did not exist, and has been created now.')
        self.db_path = os.path.join(db_dir, DBConsts.ANTHOLOGY_DB)
        self.conn = None
        self.cursor = None

        self.cache_enable = cache_enable
        if self.cache_enable:
            self.cache = LocalCache('anthology', cache_dir, self.logger)
            self.cache.smart_load()
        else:
            self.cache = None

    def db_connect(self):
        self.conn = pymysql.connect(host=MySQLCFG.HOST,
                                    port=MySQLCFG.PORT,
                                    user=MySQLCFG.USER,
                                    password=MySQLCFG.PASSWORD,
                                    db=MySQLCFG.DB,
                                    charset='utf8mb4')
        self.cursor = self.conn.cursor()

    def db_close_with_commit(self):
        self.cursor.close()
        # 提交事务:
        self.conn.commit()
        # 关闭Connection:
        self.conn.close()

    def db_close_without_commit(self):
        self.cursor.close()
        # 关闭Connection:
        self.conn.close()

    def create_tables(self):
        self.db_connect()
        # conferences
        self.cursor.execute(f'''create table if not exists {DBConsts.CONF_TABLE}(id int primary key auto_increment, 
                                conf_content varchar(20) not null, 
                                venue varchar(20), 
                                year int, 
                                link char(100), 
                                volume_size int);
                            ''')
        # papers
        self.cursor.execute(f'''create table if not exists {DBConsts.PAPER_TABLE}(id int primary key auto_increment, 
                                title varchar(1000) not null, 
                                year int, 
                                url char(100), 
                                authors text, 
                                abstract text,
                                conf_content varchar(20),
                                venue varchar(20));
                            ''')
        self.db_close_with_commit()

    def insert_a_conf_content(self, conf_content: ConfContent):
        self.cursor.execute(f'''insert ignore into {DBConsts.CONF_TABLE}
                                (conf_content, venue, year, link, volume_size)
                                values
                                ('{conf_content.name}', '{conf_content.venue}', {conf_content.year}, 
                                '{conf_content.link}', {conf_content.volume_size});
                            ''')

    def insert_a_paper(self, paper: Paper):
        title_norm = paper.title.replace("'", f"\\'")
        authors_norm = ", ".join([one.replace("'", f"\\'") for one in paper.authors])
        abstract_norm = paper.abstract.replace("'", f"\\'")
        self.cursor.execute(f'''insert ignore into {DBConsts.PAPER_TABLE}
                                (title, year, url, authors, abstract, conf_content, venue)
                                values
                                ('{title_norm}', {paper.year}, '{paper.url}', 
                                '{authors_norm}', '{abstract_norm}', '{paper.conf_content}', 
                                '{paper.venue}');
                            ''')

    def load_data(self):
        self.db_connect()
        self.logger.info("Start loading data...")
        for conf in itertools.chain(*self.anthology.confs.values()):
            # 该conf已经加载过
            if self.cache_enable and self.cache.get(conf.name, False):
                self.logger.info(f"{conf.name} found in cache.")
                continue
            else:
                self.logger.info(f"Start loading {conf.name}...")
                for conf_content in tqdm(itertools.chain(*conf.conf_contents.values()),
                                         total=conf.size,
                                         desc=f'loading {conf.name}...'):
                    # 该conf_content已经加载过
                    if self.cache_enable and self.cache.get(conf_content.name, False):
                        continue
                    else:
                        papers = self.retriever.get_paper_list_from_volumes(conf_content.venue,
                                                                            conf_content.name,
                                                                            conf_content.year,
                                                                            conf_content.link)
                        for paper in papers.items():
                            # 插入论文
                            self.insert_a_paper(paper)
                    # 插入会议
                    self.insert_a_conf_content(conf_content)
                    self.conn.commit()  # 提交数据
                    if self.cache_enable:
                        self.cache[conf_content.name] = True
                        self.cache.store()
                if self.cache_enable:
                    self.cache[conf.name] = True
                    self.cache.store()
                    self.logger.info(f"Finished!")
        self.db_close_with_commit()

    def get_conferences(self):
        self.db_connect()
        # 执行查询 SQL
        self.cursor.execute(f'SELECT * FROM `{DBConsts.CONF_TABLE}`')
        # 获取所有数据
        result = self.cursor.fetchall()
        self.db_close_without_commit()
        return result

    def size_of_confs(self):
        self.db_connect()
        # 执行查询 SQL
        self.cursor.execute(f'SELECT count(*) FROM `{DBConsts.CONF_TABLE}`')
        # 获取所有数据
        result = self.cursor.fetchall()
        self.db_close_without_commit()
        return result

    def size_of_papers(self):
        self.db_connect()
        # 执行查询 SQL
        self.cursor.execute(f'SELECT count(*) FROM `{DBConsts.PAPER_TABLE}`')
        # 获取所有数据
        result = self.cursor.fetchall()
        self.db_close_without_commit()
        return result

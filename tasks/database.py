from src.configuration.mysql_cfg import MySQLCFG

class Config(object):
    pass

class Proconfig(Config):
    pass


class Devconfig(Config):
    debug = True
    DATABASE_URI = f'mysql+pymysql://{MySQLCFG.USER}:{MySQLCFG.USER}@{MySQLCFG.HOST}:{MySQLCFG.PORT}/{MySQLCFG.DB}'
    data_host = MySQLCFG.HOST
    data_pass = MySQLCFG.PASSWORD
    data_user = MySQLCFG.USER
    database = MySQLCFG.DB
    data_port = MySQLCFG.PORT
    charset = 'utf8mb4'


database = Devconfig



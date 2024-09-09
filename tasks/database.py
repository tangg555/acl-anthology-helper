class Config(object):
    pass

class Proconfig(Config):
    pass


class Devconfig(Config):
    debug = True
    DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1:3306/target'
    data_host = '127.0.0.1'
    data_pass = 'tang555111'
    data_user = 'root'
    database = 'acl'
    data_port = 3306
    charset = 'utf8mb4'


database = Devconfig
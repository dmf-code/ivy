# _*_ coding: utf-8 _*_
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, MetaData
from ivy.abstracts.singleton import Singleton
from sqlalchemy.orm import sessionmaker
from sqlalchemy import insert
from ivy.facade import Facade


class Database(metaclass=Singleton):
    engine = None
    context = None

    def __init__(self):
        self.Base = declarative_base()
        self.session = None
        self.context = Facade().get('context')

    def connect(self, config):
        # 兼容 mysql8 默认排序规则 utf8mb4_0900_ai_ci
        # https://forums.mysql.com/read.php?50,677424,677981#msg-677981
        dsn = 'mysql+mysqlconnector://{}:{}@{}:{}/{}?charset={}&collation={}'.format(
            config['username'],
            config['password'],
            config['host'],
            config['port'],
            config['dbname'],
            config['charset'],
            'utf8mb4_unicode_ci'
        )
        # connect_args = {'init_command': "SET @@collation_connection='utf8mb4_unicode_ci'"}
        self.engine = create_engine(dsn)
        print(self.engine.url)
        if not database_exists(self.engine.url):
            create_database(self.engine.url)

    def create_table(self, table_name, fields):
        if fields is None:
            print('fields is None')
            return True

        indexes = fields.pop('index', None)
        others = fields.pop('other', None)
        """表名，创建新表"""
        table_str = "CREATE TABLE if not exists {} (".format(table_name)
        for key, value in fields.items():
            table_str += '{} {},'.format(key, value)

        for index in indexes:
            table_str += '{},'.format(index)

        table_str = table_str.rstrip(',') + ')'

        for other in others:
            table_str += '{} '.format(other)

        table_str = table_str.rstrip(' ') + ';'
        if self.context.debug():
            print(table_str)
        self.engine.execute(table_str)  # 执行sql语句
        return True

    def get_model(self, name):
        metadata = MetaData(bind=self.engine)
        metadata.reflect(self.engine, only=[name])
        Base = automap_base(metadata=metadata)
        Base.prepare()
        return Base.classes.get(name)

    def create_session(self):
        if self.engine is None:
            raise Exception('engine is None')
        self.session = sessionmaker(bind=self.engine)()
        return self.session

    def get_session(self):
        if self.session is None:
            self.create_session()
        return self.session

    def get_engine(self):
        if self.engine is None:
            raise Exception('未连接数据库')
        return self.engine

    def batch_insert(self, table_name, dataset):
        self.create_session()
        session = self.get_session()
        session.execute(
            insert(self.get_model(table_name)),
            dataset
        )
        session.commit()

    def get_auto_increment(self, database, table):
        self.create_session()
        session = self.get_session()
        row = session.execute(
            "SELECT " +
            "if(max(id), max(id), 0) AS id" +
            " from {}.{}".format(database, table)
        )
        session.commit()
        pk_id = row.fetchone()[0]
        if pk_id > 0:
            pk_id = pk_id + 1
        return pk_id

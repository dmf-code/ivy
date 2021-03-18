# _*_ coding: utf-8 _*_
from ivy.abstracts.singleton import Singleton
from sqlalchemy import create_engine
from ivy.facade import Facade
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapper
from ivy.functions import funcs
from ivy.functions.faker import fake
import copy


class Database(metaclass=Singleton):
    engine = None
    context = None

    def __init__(self):
        self.Base = declarative_base()
        self.session = None
        self.context = Facade().get('context')

    def connect(self, config):
        dsn = 'mysql+pymysql://{}:{}@{}:{}/{}?charset={}'.format(
            config['username'],
            config['password'],
            config['host'],
            config['port'],
            config['dbname'],
            config['charset']
        )
        self.engine = create_engine(dsn)
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
        """根据表名name动态创建并return一个新的model类
        name:数据库表名
        engine:create_engine返回的对象，指定要操作的数据库连接，from sqlalchemy import create_engine
        """
        self.Base.metadata.reflect(self.engine)
        table = self.Base.metadata.tables[name]
        t = type(name, (object,), dict())
        mapper(t, table)
        self.Base.metadata.clear()
        return t

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

    @staticmethod
    def custom_data_handle(func_, **kwargs):
        if funcs.get(func_, None) is None:
            raise Exception('func is not define')
        if not kwargs:
            res = funcs[func_]()
        else:
            res = funcs[func_](**kwargs)
        return res

    @staticmethod
    def faker_data_handle(func_, **kwargs):
        if not hasattr(fake, func_):
            raise Exception('faker module not have this function')
        if not kwargs:
            res = getattr(fake, func_)()
        else:
            res = getattr(fake, func_)(**kwargs)
        return res

    def fill_data(self, fill_rule, table_name):
        session = self.get_session()
        model = self.get_model(table_name)
        model_instance = model()

        for k, v in fill_rule.items():
            copy_value = copy.deepcopy(v)
            func_ = copy_value.pop('func')
            if 'faker' in func_:
                insert_value = self.faker_data_handle(func_, **copy_value)
            else:
                insert_value = self.custom_data_handle(func_, **copy_value)

            setattr(model_instance, k, insert_value)
            session.add(model_instance)
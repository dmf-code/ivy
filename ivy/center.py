# _*_ coding: utf-8 _*_
from ivy.functions.faker import fake
from ivy.functions import funcs
from ivy.facade import Facade
import copy


class Center(object):
    context = None
    database = None
    configs = None

    def __init__(self):
        self.context = Facade().get('context')
        self.database = Facade().get('database')
        self.configs = self.context.get()

        self.create_tables()

        for item in self.configs:
            dsn = {
                'host': item['host'],
                'port': item['port'],
                'username': item['username'],
                'password': item['password'],
                'charset': item['charset'],
                'dbname': item['dbname']
            }
            self.database.connect(dsn)

            for database in item['databases']:
                table_name = database.get('table', None)
                rules = database.get('rules', None)
                number = database.get('number', 0)
                chunk = database.get('chunk', 100)

                insert_list = []

                while number > 0:
                    data = self.faker(rules)
                    insert_list.append(data)
                    if len(insert_list) == chunk:
                        self.database.batch_insert(table_name, insert_list)
                        insert_list.clear()
                    number -= 1

                if len(insert_list) > 0:
                    self.database.batch_insert(table_name, insert_list)

    def create_tables(self):

        for config in self.configs:
            dsn = {
                'host': config['host'],
                'port': config['port'],
                'username': config['username'],
                'password': config['password'],
                'charset': config['charset'],
                'dbname': config['dbname']
            }

            self.database.connect(dsn)
            for database in config['databases']:
                table_name = database.get('table', None)
                table_fields = database.get('fields', None)
                self.database.create_table(table_name, table_fields)

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

    def faker(self, rules):
        data = {}
        for k, v in rules.items():
            copy_value = copy.deepcopy(v)
            func_ = copy_value.pop('func')
            if 'faker' in func_:
                insert_value = self.faker_data_handle(func_, **copy_value)
            else:
                insert_value = self.custom_data_handle(func_, **copy_value)
            data[k] = insert_value

        return data

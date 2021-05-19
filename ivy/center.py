# _*_ coding: utf-8 _*_
from ivy.functions.faker import fake
from ivy.functions import funcs
from ivy.facade import Facade
from functools import reduce
import copy


class Center(object):
    context = None
    database = None
    configs = None
    rules = {}

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

            for table in item['tables']:
                table_name = table.get('table', None)
                rules = table.get('rules', None)
                number = table.get('number', 0)
                chunk = table.get('chunk', 100)

                insert_list = []

                while number > 0:
                    if rules is None:
                        break

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
            for table in config['tables']:
                table_name = table.get('table', None)
                table_fields = table.get('fields', None)
                flag = table.get('flag', None)

                self.rules[flag] = table.get('rules', None)

                self.database.create_table(table_name, table_fields)

    @staticmethod
    def custom_data_handle(_func, **kwargs):
        if funcs.get(_func, None) is None:
            raise Exception('func is not define')
        if not kwargs:
            res = funcs[_func]()
        else:
            res = funcs[_func](**kwargs)
        return res

    @staticmethod
    def faker_data_handle(_func, **kwargs):
        if not hasattr(fake, _func):
            raise Exception('faker module not have this function')
        if not kwargs:
            res = getattr(fake, _func)()
        else:
            res = getattr(fake, _func)(**kwargs)
        return res

    def faker(self, rules):
        data = {}

        for k, v in rules.items():
            copy_value = copy.deepcopy(v)
            _func = copy_value.pop('func')
            if 'faker' in _func:
                insert_value = self.faker_data_handle(_func, **copy_value)
            else:
                insert_value = self.custom_data_handle(_func, **copy_value)
            data[k] = insert_value

        return data

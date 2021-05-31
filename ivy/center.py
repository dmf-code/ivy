# _*_ coding: utf-8 _*_
from ivy.services.batch_service import BatchService
from ivy.manages.context import Context
from ivy.facade import Facade
from ivy.const import Const
import random


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
                lines = table.get('lines', None)

                if lines is None:
                    lines = [str(random.randint(1, 100)) + '-' + table_name]

                BatchService().lines(lines, number, rules, chunk)

    def create_tables(self):
        print(self.configs)
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

            Context().set(self.rules, Const.CLASS_VAR_RULES)

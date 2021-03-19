# _*_ coding: utf-8 _*_
from ivy.facade import Facade
from sqlalchemy import insert


class Center(object):
    context = None
    database = None

    def __init__(self):
        self.context = Facade().get('context')
        self.database = Facade().get('database')
        padding_data = self.context.get()
        for item in padding_data:
            config = {
                'host': item['host'],
                'port': item['port'],
                'username': item['username'],
                'password': item['password'],
                'charset': item['charset'],
                'dbname': item['dbname']
            }
            self.database.connect(config)
            for database in item['databases']:
                table_name = database.get('table', None)
                fields = database.get('fields', None)
                rules = database.get('rules', None)
                number = database.get('number', 0)
                self.database.create_table(table_name, fields)
                insert_list = []
                self.database.create_session()
                session = self.database.get_session()
                while number > 0:
                    data = self.database.fill_data(rules, table_name)
                    insert_list.append(data)
                    number -= 1

                session.execute(
                    insert(self.database.get_model(table_name)),
                    insert_list
                )
                session.commit()

    def run(self):
        pass

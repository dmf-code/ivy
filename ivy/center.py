# _*_ coding: utf-8 _*_
from ivy.database_manage import database_manage
from ivy.global_manage import global_manage


class Center(object):
    def __init__(self):
        padding_data = global_manage.get()
        for item in padding_data:
            config = {
                'host': item['host'],
                'port': item['port'],
                'username': item['username'],
                'password': item['password'],
                'charset': item['charset'],
                'dbname': item['dbname']
            }
            database_manage.connect(config)
            for database in item['databases']:
                table_name = database['table']
                fields = database['fields']
                fill_rule = database.get('fill_rule', {})
                number = database['number']
                database_manage.create_table(table_name, fields)
                while number > 0:
                    database_manage.create_session()
                    database_manage.get_session()
                    database_manage.fill_data(fill_rule, table_name)
                    print(number)
                    number -= 1
                    database_manage.get_session().commit()

    def run(self):
        pass

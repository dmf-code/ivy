# -*- coding: utf-8 -*-
from ivy.facade import Facade


class Id(object):
    @staticmethod
    def auto_increment(**kwargs):
        database = Facade().get('database')
        database_name = kwargs.get('database', None)
        table_name = kwargs.get('table', None)
        if database_name is None or kwargs.get(table_name, None):
            raise Exception('not have database or table_name')

        return database.get_auto_increment(database_name, table_name)

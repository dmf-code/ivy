# -*- coding: utf-8 -*-
from ivy.manages.faker import Faker
from ivy.facade import Facade
import copy


class BatchService(object):

    @staticmethod
    def lines(line, number, rules, chunk):
        insert_dict = {}
        database = Facade().get('database')
        cnt = 0
        while number > 0:
            if rules is None:
                break

            data = Faker().get_line(copy.copy(line))

            for k, v in data.items():
                (flag, table_name) = k.split('-')

                if insert_dict.get(table_name, None) is None or not isinstance(insert_dict[table_name], list):
                    insert_dict[table_name] = []
                insert_dict[table_name].append(v)

            cnt = cnt + 1
            if cnt == chunk:
                for key, value in insert_dict.items():
                    database.batch_insert(key, value)
                cnt = 0
                insert_dict = {}
            number -= 1

        if cnt > 0:
            for key, value in insert_dict.items():
                database.batch_insert(key, value)

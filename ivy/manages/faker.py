# -*- coding: utf-8 -*-
from ivy.manages.context import Context
from ivy.functions.faker import faker
from ivy.functions import funcs
from ivy.const import Const
import copy


class Faker(object):
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
        name = _func.split('|')[-1]
        language = kwargs.get('lang', 'zh_CN')

        new_faker = faker.select_faker(language)

        if not hasattr(new_faker, name):
            raise Exception('faker module not have this function')

        if not kwargs:
            res = getattr(new_faker, name, language)()
        else:
            res = getattr(new_faker, name, language)(**kwargs)
        return res

    def get(self, rules):
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

    def get_line(self, line):
        line.reverse()

        while len(line) > 0:
            flag = line.pop()
            # 获取规则
            rule = Context().get(Const.CLASS_VAR_RULES + '.' + flag)
            data = self.get(rule)
            # 保存数据
            Context().set(data, Const.CLASS_VAR_CELLS + '.' + flag)

        cells = Context().get(Const.CLASS_VAR_CELLS)
        Context().clear(Const.CLASS_VAR_CELLS)
        return cells

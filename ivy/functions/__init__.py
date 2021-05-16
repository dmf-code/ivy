# -*- coding: utf-8 -*-
from ivy.functions.date import Date
from ivy.functions.default import Default

# 自定义填充函数
funcs = {
    'range_date': Date().range,
    'default': Default().default
}

# faker 函数
# 具体用法参考 https://faker.readthedocs.io/en/master/locales/zh_CN.html

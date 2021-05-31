# -*- coding: utf-8 -*-
from ivy.functions.id import Id
from ivy.functions.date import Date
from ivy.functions.cell import Cell
from ivy.functions.default import Default

# 自定义填充函数
funcs = {
    'id_auto_increment': Id().auto_increment,  # 获取自增 id
    'cell_conversion': Cell().conversion,  # pipeline 每个元素状态保存
    'date_range': Date().range,  # 日期范围随机返回
    'default': Default().default,  # 返回设置默认值
    'default_random': Default().random  # 返回配置中的随机默认值
}

# faker 函数
# 具体用法参考 https://faker.readthedocs.io/en/master/locales/zh_CN.html

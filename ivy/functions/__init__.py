# -*- coding: utf-8 -*-
from ivy.functions.date import Date
from ivy.functions.default import Default

funcs = {
    'range_date': Date().range,
    'default': Default().default
}

# -*- coding: utf-8 -*-
from ivy.manages.context import Context
from ivy.const import Const


class Cell(object):
    @staticmethod
    def conversion(**kwargs):
        cells = Context().get(Const.CLASS_VAR_CELLS)
        flag = kwargs.get('flag', None)
        name = kwargs.get('name', None)
        if cells.get(flag, None) is None:
            raise Exception('error: cell get flag')

        return cells[flag].get(name, None)

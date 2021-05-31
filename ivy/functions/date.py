# -*- coding: utf-8 -*-
from ivy.const import Const
import datetime
import random
import time


class Date(object):

    @staticmethod
    def parse_ymd(_date):
        year_str, month_str, day_str = _date.split('-')
        return datetime.datetime(int(year_str), int(month_str), int(day_str))

    @staticmethod
    def parse_stamp(_time):
        return int(time.mktime(_time))

    @staticmethod
    def handle_time(key):
        return getattr(Const, key)

    def range(self, **kwargs):
        start = kwargs.get('start', None)
        end = kwargs.get('end', None)
        start_format = kwargs.get('start_format', '%Y-%m-%d')
        end_format = kwargs.get('end_format', '%Y-%m-%d')
        res_format = kwargs.get('res_format', None)
        step = self.handle_time(kwargs.get('step', Const().DAY_TO_SECOND))
        if start is None or end is None:
            raise Exception('start or end is None')
        if isinstance(start, datetime.date):
            start = start.__str__()

        if isinstance(end, datetime.date):
            end = end.__str__()

        start_time = self.parse_stamp(time.strptime(start, start_format))
        end_time = self.parse_stamp(time.strptime(end, end_format))
        res_time = random.randrange(start_time, end_time + step, step)

        if res_format:
            res_time = time.strftime(res_format, time.localtime(res_time))

        return res_time


if __name__ == '__main__':
    number = 5
    date = Date()
    while number > 0:
        print(date.range(**{'start': '2018-08-01', 'end': '2019-08-01'}))
        number -= 1

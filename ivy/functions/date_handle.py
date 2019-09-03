# -*- coding: utf-8 -*-
from ivy import const
import datetime
import random
import time


class DateHandle(object):

    @staticmethod
    def parse_ymd(date_):
        year_s, mon_s, day_s = date_.split('-')
        return datetime.datetime(int(year_s), int(mon_s), int(day_s))

    @staticmethod
    def parse_stamp(time_):
        return int(time.mktime(time_))

    @staticmethod
    def handle_time(key):
        return getattr(const, key)

    def range(self, **kwargs):
        start = kwargs.get('start', None)
        end = kwargs.get('end', None)
        start_format = kwargs.get('start_format', '%Y-%m-%d')
        end_format = kwargs.get('end_format', '%Y-%m-%d')
        res_format = kwargs.get('res_format', None)
        step = self.handle_time(kwargs.get('step', const.DAY_TO_SECOND))
        print(step)
        if start is None or end is None:
            raise Exception('start or end is None')
        start_time = self.parse_stamp(time.strptime(start, start_format))
        end_time = self.parse_stamp(time.strptime(end, end_format))
        res_time = random.randrange(start_time, end_time + step, step)
        print(res_time)
        if res_format:
            res_time = time.strftime(res_format, time.localtime(res_time))
        return res_time


if __name__ == '__main__':
    number = 5
    date_handle = DateHandle()
    while number > 0:
        print(date_handle.range(**{'start': '2018-08-01', 'end': '2019-08-01'}))
        number -= 1

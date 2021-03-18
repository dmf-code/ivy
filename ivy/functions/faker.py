# -*- coding: utf-8 -*-
from faker.providers import BaseProvider
from faker import Faker


class FakerHandle(object):
    """
    language: 英文en_US，中文zh_CN
    """
    def __init__(self, language='zh_CN'):
        self.fake = Faker(language)

    def __getattr__(self, method_name):
        method_name = method_name.split('|')[-1]
        if not hasattr(self.fake, method_name):
            raise Exception('faker module not have this function')

        def func(**kwargs):
            if not kwargs:
                return getattr(self.fake, method_name)()
            return getattr(self.fake, method_name)(**kwargs)

        return func


fake = FakerHandle()

if __name__ == '__main__':
    fake = FakerHandle()

    print(fake.profile())
    print(fake.phone_number())



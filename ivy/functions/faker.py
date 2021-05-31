# -*- coding: utf-8 -*-
from faker import Faker


class FakerHandle(object):
    """
    language: 英文en_US，中文zh_CN
    """
    faker = {}

    def __init__(self):
        self.faker['zh_CN'] = Faker('zh_CN')
        self.faker['en_US'] = Faker('en_US')

    def select_faker(self, language):
        return self.faker[language]

    def __getattr__(self, method_name, language):
        method_name = method_name.split('|')[-1]
        select_faker = self.select_faker(language)
        if not hasattr(select_faker, method_name):
            raise Exception('faker module not have this function')

        def func(**kwargs):
            if not kwargs:
                return getattr(select_faker, method_name)()
            return getattr(select_faker, method_name)(**kwargs)

        return func


faker = FakerHandle()

if __name__ == '__main__':
    fake = FakerHandle()

    print(fake.profile())
    print(fake.phone_number())

# _*_ coding: utf-8 _*_
from ivy.abstracts.singleton import Singleton


class Context(metaclass=Singleton):
    _config = None
    _debug = True

    def set(self, value, _type='_config'):
        if getattr(self, _type) is None:
            setattr(self, _type, value)

    def get(self, key=None, _type='_config'):
        if key is None:
            return getattr(self, _type)
        return getattr(self, _type)[key]

    def debug(self):
        return self._debug


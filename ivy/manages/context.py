# _*_ coding: utf-8 _*_
from ivy.abstracts.singleton import Singleton
from ivy.const import Const
import re


class Context(metaclass=Singleton):
    _config = None
    _debug = True
    _rules = None
    _cells = {}

    def set(self, value, key='config'):
        keys = key.split('.')
        keys.reverse()
        class_var = keys.pop()
        data = getattr(self, '_' + class_var)
        if data is None:
            setattr(self, '_' + class_var, value)
        else:
            while len(keys) > 1:
                _key = keys.pop()
                if _key not in data:
                    data[key] = {}
                data = data[key]

            _key = keys.pop()
            if re.search('_custom_array', _key):
                if _key not in data or not isinstance(data[_key], list):
                    data[_key] = []
                data[_key].append(value)
            else:
                data[_key] = value

    def get(self, key='config'):
        keys = key.split('.')
        keys.reverse()
        class_var = keys.pop()
        data = getattr(self, '_' + class_var, {})

        if keys is None or keys is []:
            return data

        while len(keys) > 0:
            value = data.get(keys.pop(), None)
            if value is None:
                return value

            if len(keys) == 0:
                return value

        return data

    def clear(self, key):
        if key == Const.CLASS_VAR_CONFIG:
            setattr(self, '_config', None)
        elif key == Const.CLASS_VAR_RULES:
            setattr(self, '_rules', None)
        elif key == Const.CLASS_VAR_CELLS:
            setattr(self, '_cells', {})

    def debug(self):
        return self._debug

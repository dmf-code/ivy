# -*- coding: utf-8 -*-


class Const(object):

    DAY_TO_SECOND = 86400

    HOUR_TO_SECOND = 3600

    MINUTE_TO_SECOND = 60

    SECOND = 1

    class ConstError(TypeError):
        pass

    def __setattr__(self, key, value):

        if key in self.__dict__:
            raise (self.ConstError, "Can't rebind const instance attribute ({})".format(key))

        self.__dict__[key] = value

    def __delattr__(self, key):
        if key in self.__dict__:
            raise (self.ConstError, "Can't unbind const const instance attribute ({})".format(key))

        raise (AttributeError, "const instance has no attribute '{}'".format(key))


import sys
sys.modules[__name__] = Const()

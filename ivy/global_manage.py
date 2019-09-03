# _*_ coding: utf-8 _*_


class GlobalManage(object):
    _config = None
    __abc = {}
    _debug = True

    def set(self, value, type_='_config'):
        if getattr(self, type_) is None:
            setattr(self, type_, value)

    def get(self, key=None, type_='_config'):
        if key is None:
            return getattr(self, type_)
        return getattr(self, type_)[key]

    def debug(self):
        return self._debug


global_manage = GlobalManage()


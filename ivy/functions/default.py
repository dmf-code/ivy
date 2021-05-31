import random


class Default(object):
    @staticmethod
    def default(**kwargs):
        return kwargs.get('value', None)

    @staticmethod
    def random(**kwargs):
        arr = kwargs.get('array', None)

        if arr is None:
            raise Exception('default: array is None')
        array_len = len(arr)
        if array_len > 0:
            array_len = array_len - 1
        return arr[random.randint(0, array_len)]

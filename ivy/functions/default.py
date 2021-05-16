

class Default(object):
    @staticmethod
    def default(**kwargs):
        return kwargs.get('value', None)

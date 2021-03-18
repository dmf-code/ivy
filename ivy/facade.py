from ivy.abstracts.singleton import Singleton


class Facade(metaclass=Singleton):
    app = {}

    def set(self, name, value):
        self.app[name] = value

    def get(self, name):
        return self.app.get(name)

from abc import (abstractmethod, ABCMeta)


class Presenter(object):
    __metaclass__ = ABCMeta

    @property
    def view(self):
        pass

    @view.setter
    @abstractmethod
    def view(self, val):
        pass

    def check_view(self, val):
        if not isinstance(val, type):
            raise TypeError("Presenter: The provided view object is not of type View but of type {0}".format(type(val)))

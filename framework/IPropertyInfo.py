import abc


class IPropertyInfo(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def destroy(self):
        pass

    @property
    @abc.abstractmethod
    def name(self):
        pass

    @abc.abstractmethod
    def get_value(self):
        pass

    @abc.abstractmethod
    def set_value(self, value):
        pass

    @abc.abstractmethod
    def add_listener(self, listener):
        pass

    @abc.abstractmethod
    def remove_listener(self, listener):
        pass

import abc


class ICommand(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def can_execute(self, model):
        pass

    @abc.abstractmethod
    def execute(self, model):
        pass

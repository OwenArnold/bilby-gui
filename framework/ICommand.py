import abc


class ICommand(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def can_execute(self):
        pass

    @abc.abstractmethod
    def execute(self):
        pass

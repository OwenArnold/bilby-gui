import abc


class IBinding(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def destroy(self):
        pass

import abc


class IPropertyListener(object):
        __metaclass__ = abc.ABCMeta

        @abc.abstractmethod
        def on_property_changed(self, model, property, value):
            pass

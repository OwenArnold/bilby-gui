from IPropertyInfo import IPropertyInfo
from IPropertyListener import IPropertyListener


class AbstractPropertyInfo(IPropertyInfo):

    def __init__(self):
        super(AbstractPropertyInfo, self).__init__()

        self._listeners = []

    def add_listener(self, listener):
        if not isinstance(listener, IPropertyListener):
            raise ValueError("AbstractPropertyInfo: the specified listener is not of type IPropertyListener")
        if listener in self._listeners:
            raise ValueError("AbstractPropertyInfo: the specified listener is already registered")

        self._listeners.append(listener)

    def remove_listener(self, listener):
        if listener not in self._listeners:
            raise ValueError("AbstractPropertyInfo: the specified listener is not registered")

        self._listeners.remove(listener)

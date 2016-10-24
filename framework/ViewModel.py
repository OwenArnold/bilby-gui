from IPropertyListener import IPropertyListener


class ViewModel(object):

    def __init__(self):
        super(ViewModel, self).__init__()

        self._listeners = []

    def add_listener(self, listener):
        if not isinstance(listener, IPropertyListener):
            raise ValueError("ViewModel: the specified listener is not of type IPropertyListener")
        if listener in self._listeners:
            raise ValueError("ViewModel: the specified listener is already registered")

        self._listeners.append(listener)

    def remove_listener(self, listener):
        if listener not in self._listeners:
            raise ValueError("ViewModel: the specified listener is not registered")

        self._listeners.remove(listener)

    def notify_property_changed(self, model, property, value):
        for listener in self._listeners:
            listener.on_property_changed(model, property, value)

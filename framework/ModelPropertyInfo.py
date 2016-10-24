from AbstractPropertyInfo import AbstractPropertyInfo
from IPropertyListener import IPropertyListener


class ModelPropertyInfo(AbstractPropertyInfo):

    class VmListener(IPropertyListener):

        def __init__(self, property, listeners):
            super(ModelPropertyInfo.VmListener, self).__init__()

            self._property = property
            self._listeners = listeners

        def on_property_changed(self, model, property, value):
            if property == self._property:
                for listener in self._listeners:
                    listener.on_property_changed(model, property, value)

    def __init__(self, vm, model, property):
        super(ModelPropertyInfo, self).__init__()

        if not hasattr(model, property):
            raise ValueError("ModelPropertyInfo: the specified model doesn't have required property \"{0}\"".format(property))

        self._model = model
        self._property = property

        self._vm = vm
        self._vm_listener = ModelPropertyInfo.VmListener(self._property, self._listeners)
        self._vm.add_listener(self._vm_listener)

    def destroy(self):
        if self._vm_listener:
            self._vm.remove_listener(self._vm_listener)
            self._vm_listener = None

    @property
    def name(self):
        return self._property

    def get_value(self):
        return getattr(self._model, self._property)

    def set_value(self, value):
        setattr(self._model, self._property, value)

from BindingMode import BindingMode
from IPropertyListener import IPropertyListener


class TextBinding(object):

    class SourceListener(IPropertyListener):

        def __init__(self, property, target):
            super(TextBinding.SourceListener, self).__init__()

            self._property = property
            self._target = target

        def on_property_changed(self, model, property, value):
            if (property == self._property) and (str(self._target.text()) != value):
                self._target.setText(value)

    def __init__(self, source, property, target, mode=BindingMode.TwoWay):
        super(TextBinding, self).__init__()

        if not hasattr(source, property):
            raise ValueError("TextBinding: the specified source doesn't have required property \"{0}\"".format(property))

        if mode is BindingMode.TwoWay or mode is BindingMode.OneWay:
            self._source = source
            self._source_listener = TextBinding.SourceListener(property, target)
            self._source.add_listener(self._source_listener)
        else:
            self._source_listener = None

        if mode is BindingMode.TwoWay or mode is BindingMode.OneWayToSource:
            self._target = target
            self._target_slot = lambda text: setattr(source, property, str(text))
            self._target.textEdited.connect(self._target_slot)
        else:
            self._target_slot = None

    def destroy(self):
        try:
            if self._source_listener:
                self._source.remove_listener(self._source_listener)
                self._source_listener = None
        finally:
            if self._target_slot:
                self._target.textEdited.disconnect(self._target_slot)
                self._target_slot = None

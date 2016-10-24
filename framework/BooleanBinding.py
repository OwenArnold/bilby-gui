from IBinding import IBinding
from BindingMode import BindingMode
from IPropertyListener import IPropertyListener


class BooleanBinding(IBinding):

    class SourceListener(IPropertyListener):

        def __init__(self, property, target):
            super(BooleanBinding.SourceListener, self).__init__()

            self._property = property
            self._target = target

        def on_property_changed(self, model, property, value):
            if (property == self._property) and (self._target.isChecked() != value):
                self._target.setChecked(value)

    def __init__(self, property_info, target, mode=BindingMode.TwoWay):
        super(BooleanBinding, self).__init__()

        if mode is BindingMode.TwoWay or mode is BindingMode.OneWay:
            self._property_info = property_info
            self._property_info_listener = BooleanBinding.SourceListener(property_info.name, target)
            self._property_info.add_listener(self._property_info_listener)
        else:
            self._source_listener = None

        if mode is BindingMode.TwoWay or mode is BindingMode.OneWayToSource:
            self._target = target
            self._target_slot = lambda checked: property_info.set_value(bool(checked))
            self._target.toggled.connect(self._target_slot)
        else:
            self._target_slot = None

    def destroy(self):
        try:
            if self._property_info_listener:
                self._property_info.remove_listener(self._property_info_listener)
                self._property_info_listener = None
        finally:
            if self._target_slot:
                self._target.toggled.disconnect(self._target_slot)
                self._target_slot = None

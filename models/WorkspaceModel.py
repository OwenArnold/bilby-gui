import abc


class WorkspaceModel(object):

    class IListener(object):
        __metaclass__ = abc.ABCMeta

        @abc.abstractmethod
        def on_scattering_sample_changed(self, model, value):
            pass

        @abc.abstractmethod
        def on_scattering_empty_cell_changed(self, model, value):
            pass

        @abc.abstractmethod
        def on_transmission_empty_cell_changed(self, model, value):
            pass

        @abc.abstractmethod
        def on_debug_mode_changed(self, model, value):
            pass

    def __init__(self):
        super(WorkspaceModel, self).__init__()

        self._listeners = []

        self._scattering_sample = ""
        self._scattering_empty_cell = ""
        self._transmission_empty_cell = ""

        self._debug_mode = False

    def add_listener(self, listener):
        if not isinstance(listener, WorkspaceModel.IListener):
            raise ValueError("WorkspaceModel: the specified listener is not of type IListener")
        if listener in self._listeners:
            raise ValueError("WorkspaceModel: the specified listener is already registered")

        self._listeners.append(listener)

    def remove_listener(self, listener):
        if listener not in self._listeners:
            raise ValueError("WorkspaceModel: the specified listener is not registered")

        self._listeners.remove(listener)

    def _call_listeners(self, target):
        for listener in self._listeners:
            target(listener)

    @staticmethod
    def _validate_filename(value):
        if not isinstance(value, str):
            raise ValueError("WorkspaceModel: the specified file \"{0}\" is invalid.".format(value))

    @property
    def scattering_sample(self):
        return self._scattering_sample

    @scattering_sample.setter
    def scattering_sample(self, value):
        WorkspaceModel._validate_filename(value)
        if self._scattering_sample != value:
            self._scattering_sample = value
            self._call_listeners(lambda listener: listener.on_scattering_sample_changed(self, value))

    @property
    def scattering_empty_cell(self):
        return self._scattering_empty_cell

    @scattering_empty_cell.setter
    def scattering_empty_cell(self, value):
        WorkspaceModel._validate_filename(value)
        if self._scattering_empty_cell != value:
            self._scattering_empty_cell = value
            self._call_listeners(lambda listener: listener.on_scattering_empty_cell_changed(self, value))

    @property
    def transmission_empty_cell(self):
        return self._transmission_empty_cell

    @transmission_empty_cell.setter
    def transmission_empty_cell(self, value):
        WorkspaceModel._validate_filename(value)
        if self._transmission_empty_cell != value:
            self._transmission_empty_cell = value
            self._call_listeners(lambda listener: listener.on_transmission_empty_cell_changed(self, value))

    @property
    def debug_mode(self):
        return self._debug_mode

    @debug_mode.setter
    def debug_mode(self, value):
        if not isinstance(value, bool):
            raise ValueError("WorkspaceModel: the specified value \"{0}\" is not a boolean.".format(value))

        if self._debug_mode != value:
            self._debug_mode = value
            self._call_listeners(lambda listener: listener.on_debug_mode_changed(self, value))

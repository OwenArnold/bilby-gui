import abc


class SaveModel(object):

    class IListener(object):
        __metaclass__ = abc.ABCMeta

        @abc.abstractmethod
        def on_file_name_changed(self, model, value):
            pass

        @abc.abstractmethod
        def on_workspace_name_changed(self, model, value):
            pass

    def __init__(self):
        super(SaveModel, self).__init__()

        self._listeners = []

        self._file_name = ""
        self._workspace_name = ""

    def add_listener(self, listener):
        if not isinstance(listener, SaveModel.IListener):
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
    def _validate_string_settings(value):
        if not isinstance(value, str):
            raise ValueError("WorkspaceModel: the specified file \"{0}\" is invalid.".format(value))

    @property
    def file_name(self):
        return self._file_name

    @file_name.setter
    def file_name(self, value):
        SaveModel._validate_string_settings(value)
        if self._file_name != value:
            self._file_name = value
            self._call_listeners(lambda listener: listener.on_file_name_changed(self, value))

    @property
    def workspace_name(self):
        return self._workspace_name

    @workspace_name.setter
    def workspace_name(self, value):
        SaveModel._validate_string_settings(value)
        if self._workspace_name != value:
            self._workspace_name = value
            self._call_listeners(lambda listener: listener.on_workspace_name_changed(self, value))
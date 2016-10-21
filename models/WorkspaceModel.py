import os
import abc


class WorkspaceModel(object):

    class IListener(object):
        __metaclass__ = abc.ABCMeta

        @abc.abstractmethod
        def scattering_sample_changed(self, model, value):
            pass

        @abc.abstractmethod
        def scattering_empty_cell_changed(self, model, value):
            pass

        @abc.abstractmethod
        def transmission_empty_cell_changed(self, model, value):
            pass

    def __init__(self):
        super(WorkspaceModel, self).__init__()

        self._listeners = []

        self._scattering_sample = ""
        self._scattering_empty_cell = ""
        self._transmission_empty_cell = ""
        #self._blocked_beam = None
        #self._direct_beam = None

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
        if value != "" and (not isinstance(value, str) or not os.path.isfile(value)):
            raise ValueError("WorkspaceModel: the specified file \"{0}\" couldn't be found.".format(value))

    @property
    def scattering_sample(self):
        return self._scattering_sample

    @scattering_sample.setter
    def scattering_sample(self, value):
        self._validate_filename(value)
        if self._scattering_sample != value:
            self._scattering_sample = value
            self._call_listeners(lambda listener: listener.scattering_sample_changed(self, value))

    @property
    def scattering_empty_cell(self):
        return self._scattering_empty_cell

    @scattering_empty_cell.setter
    def scattering_empty_cell(self, value):
        self._validate_filename(value)
        if self._scattering_empty_cell != value:
            self._scattering_empty_cell = value
            self._call_listeners(lambda listener: listener.scattering_empty_cell_changed(self, value))

    @property
    def transmission_empty_cell(self):
        return self._transmission_empty_cell

    @transmission_empty_cell.setter
    def transmission_empty_cell(self, value):
        self._validate_filename(value)
        if value != self._transmission_empty_cell:
            self._transmission_empty_cell = value
            self._call_listeners(lambda listener: listener.transmission_empty_cell_changed(self, value))

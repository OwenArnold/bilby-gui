import abc
from mantid.api import IEventWorkspace


class WorkspaceModel(object):
    def __init__(self):
        super(WorkspaceModel, self).__init__()
        self._scattering_sample = None
        self._scattering_empty_cell = None
        self._transmission_empty_cell = None

    @staticmethod
    def _validate_workspace(workspace):
        if not isinstance(workspace, IEventWorkspace):
            raise ValueError("WorkspaceModel: The specified workspace is not an EventWorkspace.")

    @property
    def scattering_sample(self):
        return self._scattering_sample

    @scattering_sample.setter
    def scattering_sample(self, value):
        WorkspaceModel._validate_workspace(value)
        self._scattering_sample = value

    @property
    def scattering_empty_cell(self):
        return self._scattering_empty_cell

    @scattering_empty_cell.setter
    def scattering_empty_cell(self, value):
        WorkspaceModel._validate_workspace(value)
        self._scattering_empty_cell = value

    @property
    def transmission_empty_cell(self):
        return self._transmission_empty_cell

    @transmission_empty_cell.setter
    def transmission_empty_cell(self, value):
        WorkspaceModel._validate_workspace(value)
        self._transmission_empty_cell = value

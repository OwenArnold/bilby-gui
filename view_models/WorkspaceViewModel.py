from random import choice
import string

from framework.ModelPropertyInfo import ModelPropertyInfo
from framework.ViewModel import ViewModel
from framework.ICommand import ICommand
from models.WorkspaceModel import WorkspaceModel


class WorkspaceViewModel(ViewModel):
    SCATTERING_SAMPLE = 'scattering_sample'
    SCATTERING_EMPTY_CELL = 'scattering_empty_cell'
    TRANSMISSION_EMPTY_CELL = 'transmission_empty_cell'

    class ModelListener(WorkspaceModel.IListener):
        def __init__(self, vm):
            super(WorkspaceViewModel.ModelListener, self).__init__()
            self._vm = vm

        def on_scattering_sample_changed(self, model, value):
            self._vm.notify_property_changed(model, WorkspaceViewModel.SCATTERING_SAMPLE, value)

        def on_scattering_empty_cell_changed(self, model, value):
            self._vm.notify_property_changed(model, WorkspaceViewModel.SCATTERING_EMPTY_CELL, value)

        def on_transmission_empty_cell_changed(self, model, value):
            self._vm.notify_property_changed(model, WorkspaceViewModel.TRANSMISSION_EMPTY_CELL, value)

    def __init__(self, model):
        super(WorkspaceViewModel, self).__init__()

        self._model = model
        self._listener = WorkspaceViewModel.ModelListener(self)

        self._model.add_listener(self._listener)

        self.scattering_sample_property = ModelPropertyInfo(self, model, WorkspaceViewModel.SCATTERING_SAMPLE)
        self.scattering_empty_cell_property = ModelPropertyInfo(self, model, WorkspaceViewModel.SCATTERING_EMPTY_CELL)
        self.transmission_empty_cell_property = ModelPropertyInfo(self, model, WorkspaceViewModel.TRANSMISSION_EMPTY_CELL)

        self.load_scattering_sample_command = WorkspaceViewModel.RandomTextCommand(self._model, WorkspaceViewModel.SCATTERING_SAMPLE)
        self.clear_scattering_sample_command = WorkspaceViewModel.ClearTextCommand(self._model, WorkspaceViewModel.SCATTERING_SAMPLE)

    def destroy(self):
        self.scattering_sample_property.destroy()
        self.scattering_empty_cell_property.destroy()
        self.transmission_empty_cell_property.destroy()

    # commands
    class ClearTextCommand(ICommand):
        def __init__(self, model, property):
            super(WorkspaceViewModel.ClearTextCommand, self).__init__()

            self._model = model
            self._property = property

        def can_execute(self):
            return str(getattr(self._model, self._property)) != ""

        def execute(self):
            if not self.can_execute():
                raise RuntimeError("WorkspaceViewModel.ClearTextCommand: command cannot be executed")

            setattr(self._model, self._property, "")

    class RandomTextCommand(ICommand):
        def __init__(self, model, property):
            super(WorkspaceViewModel.RandomTextCommand, self).__init__()

            self._model = model
            self._property = property

        def can_execute(self):
            return True

        def execute(self):
            if not self.can_execute():
                raise RuntimeError("WorkspaceViewModel.RandomTextCommand: command cannot be executed")

            chars = string.letters + string.digits
            setattr(self._model, self._property, ''.join([choice(chars) for _ in range(5)]))

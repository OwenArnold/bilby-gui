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
    DEBUG_MODE = 'debug_mode'

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

        def on_debug_mode_changed(self, model, value):
            self._vm.notify_property_changed(model, WorkspaceViewModel.DEBUG_MODE, value)

    def __init__(self, model):
        super(WorkspaceViewModel, self).__init__()

        self._model = model
        self._listener = WorkspaceViewModel.ModelListener(self)

        self._model.add_listener(self._listener)

        self.scattering_sample_property = ModelPropertyInfo(self, model, WorkspaceViewModel.SCATTERING_SAMPLE)
        self.scattering_empty_cell_property = ModelPropertyInfo(self, model, WorkspaceViewModel.SCATTERING_EMPTY_CELL)
        self.transmission_empty_cell_property = ModelPropertyInfo(self, model, WorkspaceViewModel.TRANSMISSION_EMPTY_CELL)
        self.debug_mode_property = ModelPropertyInfo(self, model, WorkspaceViewModel.DEBUG_MODE)

        self.load_model_command = WorkspaceViewModel.LoadModelCommand(self._model)
        self.clear_model_command = WorkspaceViewModel.ClearModelCommand(self._model)

    def destroy(self):
        self.scattering_sample_property.destroy()
        self.scattering_empty_cell_property.destroy()
        self.transmission_empty_cell_property.destroy()

    # commands
    class LoadModelCommand(ICommand):
        def __init__(self, model):
            super(WorkspaceViewModel.LoadModelCommand, self).__init__()

            self._model = model

        def can_execute(self):
            return True

        def execute(self):
            if not self.can_execute():
                raise RuntimeError("WorkspaceViewModel.LoadModelCommand: command cannot be executed")

            def random_name(chars=(string.letters + string.digits), count=5):
                return ''.join([choice(chars) for _ in range(count)])

            self._model.scattering_sample = random_name()
            self._model.scattering_empty_cell = random_name()
            self._model.transmission_empty_cell = random_name()
            self._model.debug_mode = True

    class ClearModelCommand(ICommand):
        def __init__(self, model):
            super(WorkspaceViewModel.ClearModelCommand, self).__init__()

            self._model = model

        def can_execute(self):
            return True

        def execute(self):
            if not self.can_execute():
                raise RuntimeError("WorkspaceViewModel.ClearModelCommand: command cannot be executed")

            self._model.scattering_sample = ""
            self._model.scattering_empty_cell = ""
            self._model.transmission_empty_cell = ""
            self._model.debug_mode = False

from framework.ViewModel import ViewModel
from models.WorkspaceModel import WorkspaceModel


class WorkspaceViewModel(ViewModel):

    class ModelListener(WorkspaceModel.IListener):

        def __init__(self, vm):
            super(WorkspaceViewModel.ModelListener, self).__init__()
            self._vm = vm

        def on_scattering_sample_changed(self, model, value):
            self._vm.notify_property_changed(model, 'scattering_sample', value)

        def on_scattering_empty_cell_changed(self, model, value):
            self._vm.notify_property_changed(model, 'scattering_empty_cell', value)

        def on_transmission_empty_cell_changed(self, model, value):
            self._vm.notify_property_changed(model, 'transmission_empty_cell', value)

    def __init__(self, model):
        super(WorkspaceViewModel, self).__init__()

        self._model = model
        self._listener = WorkspaceViewModel.ModelListener(self)

        self._model.add_listener(self._listener)

    @property
    def scattering_sample(self):
        return self._model.scattering_sample

    @scattering_sample.setter
    def scattering_sample(self, value):
        self._model.scattering_sample = value

    @property
    def scattering_empty_cell(self):
        return self._model.scattering_empty_cell

    @scattering_empty_cell.setter
    def scattering_empty_cell(self, value):
        self._model.scattering_empty_cell = value

    @property
    def transmission_empty_cell(self):
        return self._model.transmission_empty_cell

    @transmission_empty_cell.setter
    def transmission_empty_cell(self, value):
        self._model.transmission_empty_cell = value

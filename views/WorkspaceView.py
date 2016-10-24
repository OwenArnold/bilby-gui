from PyQt4 import QtGui

from WorkspaceView_ui import Ui_WorkspaceView

from framework.CommandBinding import CommandBinding
from framework.BooleanBinding import BooleanBinding
from framework.TextBinding import TextBinding
from models.WorkspaceModel import WorkspaceModel
from view_models.WorkspaceViewModel import WorkspaceViewModel


class WorkspaceView(QtGui.QWidget):
    def __init__(self, parent=None):
        super(WorkspaceView, self).__init__(parent)

        self.setupModel()
        self.setupUi()

    def setupModel(self):
        self.model = WorkspaceModel()
        self.vm = WorkspaceViewModel(self.model)

    def setupUi(self):
        self.ui = Ui_WorkspaceView()
        self.ui.setupUi(self)

        self.bindings = []
        # properties
        self.bindings.append(TextBinding(self.vm.scattering_sample_property, self.ui.edt_sample))
        self.bindings.append(TextBinding(self.vm.scattering_sample_property, self.ui.edt_sample2))
        self.bindings.append(BooleanBinding(self.vm.debug_mode_property, self.ui.cbx_debug))
        self.bindings.append(BooleanBinding(self.vm.debug_mode_property, self.ui.cbx_debug2))
        # commands
        self.bindings.append(CommandBinding(self.vm.load_model_command, self.ui.btn_load_workspaces))
        self.bindings.append(CommandBinding(self.vm.clear_model_command, self.ui.btn_clear_workspaces))

    def destroy(self, destroy_window=True, destroy_sub_windows=True):
        for binding in self.bindings:
            binding.destroy()
        self.bindings[:] = []

        self.vm.destroy()

        super(WorkspaceView, self).destroy(destroy_window, destroy_sub_windows)

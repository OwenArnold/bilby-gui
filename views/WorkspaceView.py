from PyQt4 import QtGui

from WorkspaceView_ui import Ui_WorkspaceView

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
        self.bindings.append(TextBinding(self.vm, 'scattering_sample', self.ui.edt_sample))
        self.bindings.append(TextBinding(self.vm, 'scattering_sample', self.ui.edt_sample2))

    def destroy(self, destroy_window=True, destroy_sub_windows=True):
        for binding in self.bindings:
            binding.destroy()
        self.bindings[:] = []

        super(WorkspaceView, self).destroy(destroy_window, destroy_sub_windows)

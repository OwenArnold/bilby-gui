from PyQt4.QtGui import QWidget

from WorkspaceView_ui import Ui_WorkspaceView


class WorkspaceView(QWidget):
    def __init__(self, parent=None):
        super(WorkspaceView, self).__init__(parent)

        self.setupUi()

    def setupUi(self):
        self.ui = Ui_WorkspaceView()
        self.ui.setupUi(self)


from PyQt4.QtGui import QMainWindow, QApplication

from MainView import MainView
from AnstoMainView_ui import Ui_MainWindow


class AnstoMainView(QMainWindow, Ui_MainWindow, MainView):
    def __init__(self):
        super(AnstoMainView, self).__init__()
        self.setupUi(self)
        self.main_presenter = None

    def get_presenter(self):
        return self._presenter


if __name__ == "__main__":
    application = QApplication([])
    ansto_main_view = AnstoMainView()
    ansto_main_view.show()
    application.exec_()

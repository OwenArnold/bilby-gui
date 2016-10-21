from PyQt4.QtGui import QMainWindow, QApplication

from MainView_ui import Ui_MainView


class MainView(QMainWindow):
    def __init__(self):
        super(MainView, self).__init__()

        self.setupUi()

    def setupUi(self):
        self.ui = Ui_MainView()
        self.ui.setupUi(self)

if __name__ == "__main__":
    application = QApplication([])
    main_view = MainView()
    main_view.show()
    application.exec_()

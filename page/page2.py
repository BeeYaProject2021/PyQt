from PyQt5 import QtCore, QtGui, QtWidgets
from p2 import Ui_MainWindow
from PyQt5.QtWidgets import *

class initialWidget(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.nextstep.clicked.connect(self.nextstepClicked)
    def nextstepClicked(self):
        print("nextstep is clicked.")




if __name__ == '__main__':

    import sys

    app = QtWidgets.QApplication(sys.argv)
    mw = initialWidget()
    mw.show()
    sys.exit(app.exec_())

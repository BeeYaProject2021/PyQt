from PyQt5 import QtCore, QtGui, QtWidgets
from p2 import Ui_MainWindow
from page1 import initialWidget1
from PyQt5.QtWidgets import *
import sys
from PyQt5.QtGui import QDrag

class initialWidget(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.nextstep.clicked.connect(self.nextstepClicked)
        self.ui.actionNew.triggered.connect(self.Newaction)
    def nextstepClicked(self):
        print("nextstep is clicked.")
    def Newaction(self):
        print("OK")
        self.p1 = QtWidgets.QApplication(sys.argv)
        self.page1 = initialWidget1()
        self.page1.show()
        # sys.exit(self.p1.exec_())


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    mw = initialWidget()
    mw.show()
    sys.exit(app.exec_())

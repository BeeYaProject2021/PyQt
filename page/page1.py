from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QCoreApplication
from p1 import Ui_MainWindow1

class initialWidget1(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_MainWindow1()
        self.ui.setupUi(self)
        self.ui.CNN.hide()
        self.ui.DQN.hide()
        self.ui.GAN.hide()
        self.ui.tool1.clicked.connect(self.tool1Clicked)
        self.ui.tool2.clicked.connect(self.tool2Clicked)
        self.ui.tool3.clicked.connect(self.tool3Clicked)
        self.ui.pushButton.clicked.connect(QCoreApplication.instance().quit)
    def tool1Clicked(self):
        print("CNN is clicked.")
        self.ui.DQN.hide()
        self.ui.GAN.hide()
        self.ui.CNN.show()

    def tool2Clicked(self):
        print("DNQ is clicked.")
        self.ui.CNN.hide()
        self.ui.GAN.hide()
        self.ui.DQN.show()

    def tool3Clicked(self):
        print("GAN is clicked.")
        self.ui.CNN.hide()
        self.ui.DQN.hide()
        self.ui.GAN.show()


if __name__ == '__main__':

    import sys

    app = QtWidgets.QApplication(sys.argv)
    mw = initialWidget1()
    mw.show()
    sys.exit(app.exec_())
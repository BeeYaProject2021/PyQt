from PyQt5 import QtCore, QtGui, QtWidgets
from p3 import Ui_MainWindow

class initialWidget(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

if __name__ == '__main__':

    import sys

    app = QtWidgets.QApplication(sys.argv)
    mw = initialWidget()
    mw.show()
    sys.exit(app.exec_())
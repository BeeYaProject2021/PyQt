from PyQt5 import QtCore, QtGui, QtWidgets
from p2 import Ui_MainWindow2
from p1 import Ui_MainWindow1
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import *

import sys
from PyQt5.QtCore import QPoint, Qt, QMimeData
from PyQt5.QtGui import QDrag
from PyQt5.QtWidgets import QPushButton, QWidget, QApplication

global cp
cp = 0

class initialWidget(QtWidgets.QMainWindow):
    if cp == 0:
        print("initialWidget")
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.ui = Ui_MainWindow2()
            self.ui.setupUi(self)
            self.show()
            self.ui.nextstep.clicked.connect(self.nextstepClicked)
            self.ui.actionNew.triggered.connect(self.Newaction)
            # self.ui.actionNew = initialWidget1()
            # self.ui.conv2D_2.clicked.connect(self.move)
        def nextstepClicked(self):
            print("nextstep is clicked.")
        
        def Newaction(self):
            print("OK")
            global cp
            cp = 1
            print(cp)
            
    elif cp == 1:
        print("initialWidget1")
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.ui = Ui_MainWindow1()
            self.ui.setupUi(self)
            self.show()
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

        def closeEvent(self, event):
            print("close chose")
            global cp
            cp = 0
            print(cp)

        # self = initialWidget1()
    #     self.p1 = QtWidgets.QApplication(sys.argv)
    #     self.page1 = initialWidget1()
        
    #     self.setGeometry(605, 100, 900, 771)
    #     self.setWindowTitle('Newaction')
    #     self.page1.show()
    
    
    # def move(self):
    #     def mousePressEvent(self, e):

    #         super().mousePressEvent(e)

    #         if e.button() == Qt.LeftButton:
    #             print('press')
    # def closeEvent(self, event):
    #     QApplication.closeAllWindows()

# class initialWidget1(QtWidgets.QMainWindow):
#     print("initialWidget1")
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.ui = Ui_MainWindow1()
#         self.ui.setupUi(self)
#         self.show()
#         self.ui.CNN.hide()
#         self.ui.DQN.hide()
#         self.ui.GAN.hide()
#         self.ui.tool1.clicked.connect(self.tool1Clicked)
#         self.ui.tool2.clicked.connect(self.tool2Clicked)
#         self.ui.tool3.clicked.connect(self.tool3Clicked)
#         self.ui.pushButton.clicked.connect(QCoreApplication.instance().quit)
#     def tool1Clicked(self):
#         print("CNN is clicked.")
#         self.ui.DQN.hide()
#         self.ui.GAN.hide()
#         self.ui.CNN.show()

#     def tool2Clicked(self):
#         print("DNQ is clicked.")
#         self.ui.CNN.hide()
#         self.ui.GAN.hide()
#         self.ui.DQN.show()

#     def tool3Clicked(self):
#         print("GAN is clicked.")
#         self.ui.CNN.hide()
#         self.ui.DQN.hide()
#         self.ui.GAN.show()

#     def closeEvent(self, event):
#         print("close chose")
#         global cp
#         cp = 0
#         print(cp)
#         slef = initialWidget()


if __name__ == '__main__':

    if cp == 0:
        app = QtWidgets.QApplication(sys.argv)
        mw = initialWidget()
        sys.exit(app.exec_())
    else:
        appNewaction = QtWidgets.QApplication(sys.argv)
        p1 = initialWidget()
        sys.exit(appNewaction.exec_())

    # appNewaction = QtWidgets.QApplication(sys.argv)
    # p1 = initialWidget1()
    # sys.exit(appNewaction.exec_())
from PyQt5 import QtCore, QtGui, QtWidgets
from p2 import Ui_MainWindow2
from p1 import Ui_MainWindow1

import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Lablemove(QLabel):
    epos = QPoint()
    
    def __init__(self, title, parent):
        super().__init__(title, parent)
        self.setAcceptDrops(True)

    def mouseMoveEvent(self, e):

        if e.buttons() != Qt.RightButton:
            return

        mimeData = QMimeData()
        mimeData.setText("HI")

        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())
        self.epos = e.pos()
        dropAction = drag.exec_(Qt.MoveAction)
    
    def mousePressEvent(self, e):

        super().mousePressEvent(e)

        if e.button() == Qt.LeftButton:
            print('press')

#main page
class initialWidget(QtWidgets.QMainWindow):
    
    print("initialWidget")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_MainWindow2()
        self.ui.setupUi(self)

        self.chosepage = initialWidget1() # chosepage is other page

        self.ui.nextstep.clicked.connect(self.nextstepClicked)
        self.ui.actionNew.triggered.connect(self.chosepage.show) # isCheck action button show chosepage
        self.ui.conv2D.clicked.connect(self.action_conv2D)
        self.ui.maxpooling2D.clicked.connect(self.action_maxpooling2D)
        self.ui.flatten.clicked.connect(self.action_flatten)
        self.ui.dense.clicked.connect(self.action_dense)
        self.initUI()
    
    def initUI(self):
        self.setAcceptDrops(True)    
        self.moveconv2D = Lablemove('conv2D', self)
        self.moveconv2D.hide()
        self.movemaxpooling2D = Lablemove('maxpooling2D', self)
        self.movemaxpooling2D.hide()
        self.moveflatten = Lablemove('flatten', self)
        self.moveflatten.hide()
        self.movedense = Lablemove('dense', self)
        self.movedense.hide()

    def nextstepClicked(self):
        print("nextstep is clicked.")

    def action_conv2D(self, e):
        print("conv2D")
        # self.moveconv2D.move(50, 400)
        self.moveconv2D.show()
        self.moveconv2D.move(50, 120)

    def action_maxpooling2D(self, e):
        print("maxpooling2D")
        self.movemaxpooling2D.show()
        self.movemaxpooling2D.move(30, 190)
    
    def action_flatten(self, e):
        print("flatten")
        self.moveflatten.show()
        self.moveflatten.move(53, 260)
    
    def action_dense(self, e):
        print("dense")
        self.movedense.show()
        self.movedense.move(55, 330)
    
    def dragEnterEvent(self, e):
        e.accept()
    
    def dragMoveEvent(self, e):
        # self.conv2D.move(e.pos() - self.conv2D.epos)
        # e.accept()
        # self.maxpooling2D.move(e.pos() - self.maxpooling2D.epos)
        # e.accept()
        # self.flatten.move(e.pos() - self.flatten.epos)
        # e.accept()
        # self.dense.move(e.pos() - self.dense.epos)
        e.source().move(e.pos() - e.source().epos)

        e.accept()

    def dropEvent(self, e):
        # self.conv2D.move(e.pos() - self.conv2D.epos)
        # e.setDropAction(Qt.MoveAction)
        # e.accept()
        # self.maxpooling2D.move(e.pos() - self.maxpooling2D.epos)
        # e.setDropAction(Qt.MoveAction)
        # e.accept()
        # self.flatten.move(e.pos() - self.flatten.epos)
        # e.setDropAction(Qt.MoveAction)
        # e.accept()
        # self.dense.move(e.pos() - self.dense.epos)

        e.source().move(e.pos() - e.source().epos)
        e.setDropAction(Qt.MoveAction)
        e.accept()
    


        
#chosepage
class initialWidget1(QtWidgets.QMainWindow):
    print("initialWidget1")
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
        # self.ui.pushButton.clicked.connect(QCoreApplication.instance().quit) #close all page
        self.ui.pushButton.clicked.connect(self.close) #only colse now page
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
        slef = initialWidget()


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    mw = initialWidget()
    mw.show()
    sys.exit(app.exec_())

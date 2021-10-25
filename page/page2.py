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
        mimeData = QMimeData()

        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())
        self.epos = e.pos()
        dropAction = drag.exec_(Qt.MoveAction)

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
        self.ui.actionOpen_file.triggered.connect(self.open_file)
        self.ui.actionOpen_folder.triggered.connect(self.open_folder)
        self.ui.conv2D.clicked.connect(self.action_conv2D)
        self.ui.maxpooling2D.clicked.connect(self.action_maxpooling2D)
        self.ui.flatten.clicked.connect(self.action_flatten)
        self.ui.dense.clicked.connect(self.action_dense)
        self.ui.garbage_can.setStyleSheet(  "background-image: url(garbage_icon);" +
                                            "background-position:center;" +
                                            "background-repeat:no-repeat;" +
                                            "border: 2px solid black;")
        self.ui.scrollArea_2.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.ui.scrollArea_2.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.ui.garbage_can.clicked.connect(self.clickcan)
        self.initUI()
    
    def initUI(self):
        self.setAcceptDrops(True)    

    def nextstepClicked(self):
        print("nextstep is clicked.")

    def open_file(self):
        print("open files")
        filename, filetype = QFileDialog.getOpenFileName(self,
                  "Open file",
                  "./")                 # start path
        print(filename, filetype)
        self.ui.show_file_path.setText(filename)

    def open_folder(self):
        print("open folder")
        folder_path = QFileDialog.getExistingDirectory(self,
                  "Open folder",
                  "./")                 # start path
        print(folder_path)
        self.ui.show_folder_path.setText(folder_path)

    def action_conv2D(self):
        print("conv2D")
        userconv2D = Lablemove('conv2D', self)
        userconv2D.resize(120, 120)
        userconv2D.setAlignment(QtCore.Qt.AlignCenter)
        movie = QMovie("conv2D.gif") # Create a QMovie from our gif
        userconv2D.setMovie(movie)
        userconv2D.move(50, 120)
        userconv2D.show()
        movie.start()
    def action_maxpooling2D(self):
        print("maxpooling2D")
        usermaxpooling2D = Lablemove('maxpooling2D', self)
        usermaxpooling2D.resize(120, 120)
        usermaxpooling2D.setAlignment(QtCore.Qt.AlignCenter)
        movie = QMovie("maxpooling2D.gif")
        usermaxpooling2D.setMovie(movie)
        usermaxpooling2D.move(30, 190)
        usermaxpooling2D.show()
        movie.start()
    def action_flatten(self):
        print("flatten")
        userflatten = Lablemove('flatten', self)
        userflatten.resize(120, 120)
        userflatten.setAlignment(QtCore.Qt.AlignCenter)
        movie = QMovie("flatten.gif")
        userflatten.setMovie(movie)
        userflatten.move(53, 260)
        userflatten.show()
        movie.start()
    def action_dense(self):
        print("dense")
        userdense = Lablemove('dense', self)
        userdense.resize(120, 120)
        userdense.setAlignment(QtCore.Qt.AlignCenter)
        userdense.setStyleSheet("background-image: url(puzzle_yellow_icon);")
        userdense.move(55, 330)
        userdense.show()

    def clickcan(self):
        print("This is garbage")

    def dragEnterEvent(self, e):
        e.accept()
    
    def dragMoveEvent(self, e):
 
        e.source().move(e.pos() - e.source().epos)
        e.accept()

    def dropEvent(self, e):
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

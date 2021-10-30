from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import os
import sys


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


class Layermodel(QWidget):
    def __init__(self, *args, **kwargs):
        super(Layermodel, self).__init__(*args, **kwargs)

        self.vlayout = QVBoxLayout()
        # self.vlayout.addStretch(1)

        self.conv2D = QPushButton('conv2D')
        self.vlayout.addWidget(self.conv2D)
        # self.vlayout.addStretch(3)

        self.maxpooling2D = QPushButton('maxpooling2D')
        self.vlayout.addWidget(self.maxpooling2D)
        # self.vlayout.addStretch(3)

        self.flatten = QPushButton('flatten')
        self.vlayout.addWidget(self.flatten)
        # self.vlayout.addStretch(3)

        self.dense = QPushButton('dense')
        self.vlayout.addWidget(self.dense)
        self.vlayout.addStretch(6)
        self.garbage_can = QPushButton()
        self.garbage_can.setStyleSheet("background-image:url(./image/garbage.png);" +
                                       "background-position:center;" +
                                       "background-repeat:no-repeat;" +
                                       "border:2px solid black;" +
                                       "height:100px")

        self.vlayout.addWidget(self.garbage_can)

        self.vlayout.addStretch()
        self.setLayout(self.vlayout)


class ScrollWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super(ScrollWidget, self).__init__(*args, **kwargs)

        formLayout = QFormLayout()
        groupBox = QGroupBox()

        for n in range(100):
            label1 = QLabel('Slime_%2d' % n)
            label2 = QLabel()
            label2.setPixmap(QPixmap('./image/save'))
            formLayout.addRow(label1, label2)

        groupBox.setLayout(formLayout)

        scroll = QScrollArea()
        scroll.setWidget(groupBox)
        scroll.setWidgetResizable(True)

        layout = QVBoxLayout(self)
        layout.addWidget(scroll)


class ModelWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super(ModelWidget, self).__init__(*args, **kwargs)

        self.hlayout = QHBoxLayout()
        # self.hlayout.addStretch(10)

        self.layerm = Layermodel()
        self.hlayout.addWidget(self.layerm)

        # self.hlayout.addStretch(10)

        self.setLayout(self.hlayout)

        # self.hlayout.addStretch(1)
        self.sw = ScrollWidget()
        self.hlayout.addWidget(self.sw)
        self.hlayout.addStretch(1)

        self.layerm.conv2D.clicked.connect(self.action_conv2D)
        self.layerm.maxpooling2D.clicked.connect(self.action_maxpooling2D)
        self.layerm.flatten.clicked.connect(self.action_flatten)
        self.layerm.dense.clicked.connect(self.action_dense)
        self.setAcceptDrops(True)
        # self.show()

    def action_conv2D(self):
        print("conv2D")
        userconv2D = Lablemove('conv2D', self)
        userconv2D.resize(120, 120)
        userconv2D.setAlignment(QtCore.Qt.AlignCenter)
        movie = QMovie("./image/conv2D.gif")  # Create a QMovie from our gif
        userconv2D.setMovie(movie)
        print(self.layerm.conv2D.pos())
        userconv2D.move(self.layerm.conv2D.pos() +
                        self.layerm.pos()+QPoint(130, 0))
        # userconv2D.move(50, 120)
        userconv2D.show()
        movie.start()

    def action_maxpooling2D(self):
        print("maxpooling2D")
        usermaxpooling2D = Lablemove('maxpooling2D', self)
        usermaxpooling2D.resize(120, 120)
        usermaxpooling2D.setAlignment(QtCore.Qt.AlignCenter)
        movie = QMovie("./image/maxpooling2D.gif")
        usermaxpooling2D.setMovie(movie)
        usermaxpooling2D.move(30, 190)
        usermaxpooling2D.show()
        movie.start()

    def action_flatten(self):
        print("flatten")
        userflatten = Lablemove('flatten', self)
        userflatten.resize(120, 120)
        userflatten.setAlignment(QtCore.Qt.AlignCenter)
        movie = QMovie("./image/flatten.gif")
        userflatten.setMovie(movie)
        userflatten.move(53, 260)
        userflatten.show()
        movie.start()

    def action_dense(self):
        print("dense")
        userdense = Lablemove('dense', self)
        userdense.resize(120, 120)
        userdense.setAlignment(QtCore.Qt.AlignCenter)
        userdense.setStyleSheet(
            "background-image: url(./image/puzzle_yellow_icon);")
        userdense.move(55, 330)
        userdense.show()

    def dragEnterEvent(self, e):
        e.accept()

    def dragMoveEvent(self, e):

        e.source().move(e.pos() - e.source().epos)
        e.accept()

    def dropEvent(self, e):
        e.accept()

from re import S
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from graphics_view import *

import os
import sys


class Lablemove(QLabel):
    epos = QPoint()

    def __init__(self, title, parent):
        super().__init__(title, parent)
        self.setAcceptDrops(True)

    def mouseMoveEvent(self, e):
        mimeData = QMimeData()
        mimeData.setText(self.text())
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())
        self.epos = e.pos()
        dropAction = drag.exec_(Qt.MoveAction)


class Layermodel(QWidget):
    def __init__(self, *args, **kwargs):
        super(Layermodel, self).__init__(*args, **kwargs)

        self.vlayout = QVBoxLayout()
        self.vlayout.addSpacing(20)

        self.conv2D = Lablemove('conv2D', self)
        self.vlayout.addWidget(self.conv2D)
        self.vlayout.addSpacing(10)

        self.maxpooling2D = Lablemove('maxpooling2D', self)
        self.vlayout.addWidget(self.maxpooling2D)
        self.vlayout.addSpacing(10)

        self.flatten = Lablemove('flatten', self)
        self.vlayout.addWidget(self.flatten)
        self.vlayout.addSpacing(10)

        self.dense = Lablemove('dense', self)
        self.vlayout.addWidget(self.dense)
        self.vlayout.addStretch()
        self.garbage_can = QPushButton()
        self.garbage_can.setStyleSheet("background-image:url(./image/garbage.png);" +
                                       "background-position:center;" +
                                       "background-repeat:no-repeat;" +
                                       "border:2px solid black;" +
                                       "height:100px")

        self.vlayout.addWidget(self.garbage_can)

        self.setLayout(self.vlayout)


class ConvWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.convLayout = QVBoxLayout()
        self.btn = QPushButton("convolution")
        self.convLayout.addWidget(self.btn)
        self.convfilter =  QLineEdit()
        self.convLayout.addWidget(self.convfilter)
        self.convkernel_size = QSpinBox()
        self.convkernel_size.setRange(0,10)
        self.convLayout.addWidget(self.convkernel_size)
        self.convpadding = QComboBox()
        paddingbox = ['same', 'haha', 'lala', 'nothing']
        self.convpadding.addItems(paddingbox)
        self.convLayout.addWidget(self.convpadding)
        self.convactivation = QComboBox()
        activationbox = ['rule', 'haha', 'lala']
        self.convactivation.addItems(activationbox)
        self.convLayout.addWidget(self.convactivation)
        self.setLayout(self.convLayout)


class MaxpoolWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.maxpoolLayout = QVBoxLayout()
        self.btn = QPushButton("maxpooling")
        self.maxpoolLayout.addWidget(self.btn)
        self.maxpoolpool_size = QSpinBox()
        self.maxpoolpool_size.setRange(0,10)
        self.maxpoolLayout.addWidget(self.maxpoolpool_size)
        self.setLayout(self.maxpoolLayout)


class FlatWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.flatLayout = QVBoxLayout()
        self.btn = QPushButton("flatten")
        self.flatLayout.addWidget(self.btn)
        self.setLayout(self.flatLayout)


class DenseWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.denseLayout = QVBoxLayout()
        self.btn = QPushButton("dense")
        self.denseLayout.addWidget(self.btn)
        self.denseunits = QLineEdit()
        self.denseLayout.addWidget(self.denseunits)
        self.denseactivation = QComboBox()
        activationbox = ['rule', 'haha', 'lala']
        self.denseactivation.addItems(activationbox)
        self.denseLayout.addWidget(self.denseactivation)
        self.setLayout(self.denseLayout)


class ModelWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.hlayout = QHBoxLayout()

        self.layerm = Layermodel()
        self.hlayout.addWidget(self.layerm)

        self.vw = ViewWidget()
        self.hlayout.addWidget(self.vw)

        self.convWidget = ConvWidget()
        self.maxpoolWidget = MaxpoolWidget()
        self.flatWidget = FlatWidget()
        self.denseWidget = DenseWidget()
        self.stackWidget = QStackedWidget()
        self.stackWidget.setFixedWidth(200)
        self.stackWidget.addWidget(self.convWidget)
        self.stackWidget.addWidget(self.maxpoolWidget)
        self.stackWidget.addWidget(self.flatWidget)
        self.stackWidget.addWidget(self.denseWidget)
        self.hlayout.addWidget(self.stackWidget)
        self.setLayout(self.hlayout)
        self.vw.gv.graphics_scene.show_attribute_signal.connect(
            self.showAttributeSignal)
        self.stackWidget.setCurrentIndex(0)

    def showAttributeSignal(self, msg):
        self.stackWidget.setCurrentIndex(msg)

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
        self.setAlignment(Qt.AlignCenter)

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

        # Shadow
        self.shadow1 = QGraphicsDropShadowEffect()
        self.shadow1.setColor(QColor(62, 122, 122))
        self.shadow1.setOffset(0, 0)
        self.shadow1.setBlurRadius(5)
        self.shadow2 = QGraphicsDropShadowEffect()
        self.shadow2.setColor(QColor(62, 122, 122))
        self.shadow2.setOffset(0, 0)
        self.shadow2.setBlurRadius(5)
        self.shadow3 = QGraphicsDropShadowEffect()
        self.shadow3.setColor(QColor(62, 122, 122))
        self.shadow3.setOffset(0, 0)
        self.shadow3.setBlurRadius(5)
        self.shadow4 = QGraphicsDropShadowEffect()
        self.shadow4.setColor(QColor(62, 122, 122))
        self.shadow4.setOffset(0, 0)
        self.shadow4.setBlurRadius(5)

        self.vlayout = QVBoxLayout()
        self.vlayout.addSpacing(20)

        # Conv2D and Image
        self.conv2D_hlayout = QHBoxLayout()
        self.conv2D = Lablemove('conv2D', self)
        self.conv2D.setObjectName("conv")
        self.conv2D.setGraphicsEffect(self.shadow1)

        self.img_conv2D = QLabel()
        self.img_conv2D.setPixmap(QPixmap("./image/conv2D.png"))
        self.img_conv2D.setFixedSize(100, 100)
        self.img_conv2D.setScaledContents(True)
        self.conv2D_hlayout.addWidget(self.conv2D)
        self.conv2D_hlayout.addWidget(self.img_conv2D)

        self.vlayout.addLayout(self.conv2D_hlayout)
        self.vlayout.addSpacing(10)

        # Maxpooling and Image
        self.max_hlayout = QHBoxLayout()
        self.maxpooling = Lablemove('maxpooling2D', self)
        self.maxpooling.setObjectName("maxpooling")
        self.maxpooling.setGraphicsEffect(self.shadow2)

        self.img_pooling = QLabel()
        self.img_pooling.setPixmap(QPixmap("./image/maxpooling.png"))
        self.img_pooling.setFixedSize(100, 100)
        self.img_pooling.setScaledContents(True)
        self.max_hlayout.addWidget(self.maxpooling)
        self.max_hlayout.addWidget(self.img_pooling)

        self.vlayout.addLayout(self.max_hlayout)
        self.vlayout.addSpacing(10)

        # Flatten and Image
        self.flatten_hlayout = QHBoxLayout()
        self.flatten = Lablemove('flatten', self)
        self.flatten.setObjectName("flatten")
        self.flatten.setGraphicsEffect(self.shadow3)

        self.img_flatten = QLabel()
        self.img_flatten.setPixmap(QPixmap("./image/flatten.png"))
        self.img_flatten.setFixedSize(100, 100)
        self.img_flatten.setScaledContents(True)
        self.flatten_hlayout.addWidget(self.flatten)
        self.flatten_hlayout.addWidget(self.img_flatten)

        self.vlayout.addLayout(self.flatten_hlayout)
        self.vlayout.addSpacing(10)

        # Dense and Image
        self.dense_hlayout = QHBoxLayout()
        self.dense = Lablemove('dense', self)
        self.dense.setObjectName("dense")
        self.dense.setGraphicsEffect(self.shadow4)

        self.img_dense = QLabel()
        self.img_dense.setPixmap(QPixmap("./image/dense.png"))
        self.img_dense.setFixedSize(100, 100)
        self.img_dense.setScaledContents(True)
        self.dense_hlayout.addWidget(self.dense)
        self.dense_hlayout.addWidget(self.img_dense)

        self.vlayout.addLayout(self.dense_hlayout)
        self.vlayout.addStretch()

        self.garbage_can = QPushButton()
        self.garbage_can.setStyleSheet("background-image:url(./image/garbage.png);" +
                                       "background-position:center;" +
                                       "background-repeat:no-repeat;" +
                                       "border:2px solid black;" +
                                       "height:100px")

        self.vlayout.addWidget(self.garbage_can)

        with open("./stylesheet/model.qss", "r") as f:
            self.setStyleSheet(f.read())

        self.setLayout(self.vlayout)


class ConvWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.convLayout = QVBoxLayout()
        self.btn = QPushButton("convolution")
        self.convLayout.addWidget(self.btn)
        self.convfilter = QLineEdit()
        self.convLayout.addWidget(self.convfilter)
        self.convkernel_size = QSpinBox()
        self.convkernel_size.setRange(0, 10)
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
        self.maxpoolpool_size.setRange(0, 10)
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

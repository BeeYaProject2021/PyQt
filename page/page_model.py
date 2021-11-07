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

        self.input = Lablemove('input', self)
        self.input.setObjectName("input")
        self.vlayout.addWidget(self.input)

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

        # Maxpooling and Image
        self.pool_hlayout = QHBoxLayout()
        self.pooling = Lablemove('pooling2D', self)
        self.pooling.setObjectName("pooling")
        self.pooling.setGraphicsEffect(self.shadow2)

        self.img_pooling = QLabel()
        self.img_pooling.setPixmap(QPixmap("./image/maxpooling.png"))
        self.img_pooling.setFixedSize(100, 100)
        self.img_pooling.setScaledContents(True)
        self.pool_hlayout.addWidget(self.pooling)
        self.pool_hlayout.addWidget(self.img_pooling)

        self.vlayout.addLayout(self.pool_hlayout)

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

        self.output = Lablemove('output', self)
        self.output.setObjectName("output")
        self.vlayout.addWidget(self.output)

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
    id = 1

    def __init__(self):
        super().__init__()
        self.convLayout = QVBoxLayout()

        self.btn = QPushButton("convolution")
        self.convLayout.addWidget(self.btn)
        self.convLayout.addStretch()

        self.hfilter = QHBoxLayout()
        self.convfilterlabel = QLabel("Filter : ")
        self.hfilter.addWidget(self.convfilterlabel)
        self.convfilter = QSpinBox()
        self.convfilter.setMinimum(0)
        # self.convfilter.setSingleStep(2)
        self.hfilter.addWidget(self.convfilter)
        self.convLayout.addLayout(self.hfilter)

        self.hkernel_size = QHBoxLayout()
        self.convkernel_sizelabel = QLabel("Kernel Size : ")
        self.hkernel_size.addWidget(self.convkernel_sizelabel)
        self.convkernel_size = QSpinBox()
        self.convkernel_size.setRange(0, 99)
        self.hkernel_size.addWidget(self.convkernel_size)
        self.convLayout.addLayout(self.hkernel_size)

        self.hpadding = QHBoxLayout()
        self.convpaddinglabel = QLabel("Padding : ")
        self.hpadding.addWidget(self.convpaddinglabel)
        self.convpadding = QComboBox()
        paddingbox = ['same', 'valid']
        self.convpadding.addItems(paddingbox)
        self.hpadding.addWidget(self.convpadding)
        self.convLayout.addLayout(self.hpadding)

        self.hactivation = QHBoxLayout()
        self.convactivationlabel = QLabel("Activation : ")
        self.hactivation.addWidget(self.convactivationlabel)
        self.convactivation = QComboBox()
        activationbox = ['relu', 'sigmoid', 'softmax', 'tanh', 'deserialize',
                         'elu', 'exponential', 'gelu', 'get', 'hard_sigmoid',
                         'linear', 'selu', 'serialize', 'softmax', 'softplus',
                         'softsign', 'swish']
        self.convactivation.addItems(activationbox)
        self.hactivation.addWidget(self.convactivation)
        self.convLayout.addLayout(self.hactivation)

        self.convLayout.addStretch()
        # self.hsubmit = QHBoxLayout()
        # self.hsubmit.addStretch(5)
        # self.convsubmit = QPushButton("Submit")
        # self.hsubmit.addWidget(self.convsubmit)
        # self.convLayout.addLayout(self.hsubmit)

        self.setLayout(self.convLayout)


class MaxpoolWidget(QWidget):
    id = 2

    def __init__(self):
        super().__init__()
        self.poolLayout = QVBoxLayout()

        self.btn = QPushButton("maxpooling")
        self.poolLayout.addWidget(self.btn)
        self.poolLayout.addStretch()

        self.hchoosepool = QHBoxLayout()
        self.choosepoollable = QLabel("Choose pooling : ")
        self.hchoosepool.addWidget(self.choosepoollable)
        self.choosepool = QComboBox()
        poolstyle = ['max', 'avg']
        self.choosepool.addItems(poolstyle)
        self.hchoosepool.addWidget(self.choosepool)
        self.poolLayout.addLayout(self.hchoosepool)

        self.hpoolpool_size = QHBoxLayout()
        self.poolpool_sizelabel = QLabel("Pool Size : ")
        self.hpoolpool_size.addWidget(self.poolpool_sizelabel)
        self.poolLayout.addWidget(self.btn)
        self.poolpool_size = QSpinBox()
        self.poolpool_size.setRange(0, 10)
        self.hpoolpool_size.addWidget(self.poolpool_size)
        self.poolLayout.addLayout(self.hpoolpool_size)

        self.poolLayout.addStretch()
        self.setLayout(self.poolLayout)


class FlatWidget(QWidget):
    id = 3

    def __init__(self):
        super().__init__()
        self.flatLayout = QVBoxLayout()
        self.btn = QPushButton("flatten")
        self.flatLayout.addWidget(self.btn)
        self.flatLayout.addStretch()
        self.setLayout(self.flatLayout)


class DenseWidget(QWidget):
    id = 4

    def __init__(self):
        super().__init__()
        self.denseLayout = QVBoxLayout()
        self.btn = QPushButton("dense")
        self.denseLayout.addWidget(self.btn)
        self.denseLayout.addStretch()

        self.hdenseuiits = QHBoxLayout()
        self.denseunitslabel = QLabel("Units : ")
        self.hdenseuiits.addWidget(self.denseunitslabel)
        self.denseunits = QSpinBox()
        self.denseunits.setRange(0, 100)
        self.hdenseuiits.addWidget(self.denseunits)
        self.denseLayout.addItem(self.hdenseuiits)

        self.hdenseactivation = QHBoxLayout()
        self.denseactivationlabel = QLabel("Activation :")
        self.hdenseactivation.addWidget(self.denseactivationlabel)
        self.denseactivation = QComboBox()
        activationbox = ['relu', 'sigmoid', 'softmax', 'tanh', 'deserialize',
                         'elu', 'exponential', 'gelu', 'get', 'hard_sigmoid',
                         'linear', 'selu', 'serialize', 'softmax', 'softplus',
                         'softsign', 'swish']
        self.denseactivation.addItems(activationbox)
        self.hdenseactivation.addWidget(self.denseactivation)
        self.denseLayout.addLayout(self.hdenseactivation)

        self.denseLayout.addStretch()
        self.setLayout(self.denseLayout)


class InputWidget(QWidget):
    id = 5

    def __init__(self):
        super().__init__()
        self.inputLayout = QVBoxLayout()
        self.inputLayout.addStretch()
        self.btn = QPushButton("input")
        self.inputLayout.addWidget(self.btn)
        self.inputLayout.addStretch()
        self.setLayout(self.inputLayout)


class OutputWidget(QWidget):
    id = 6

    def __init__(self):
        super().__init__()
        self.outputLayout = QVBoxLayout()
        self.outputLayout.addStretch()
        self.btn = QPushButton("output")
        self.outputLayout.addWidget(self.btn)
        self.outputLayout.addStretch()
        self.setLayout(self.outputLayout)


class ModelWidget(QWidget):
    attr_widget = []
    layer_index_order = []

    def __init__(self):
        super().__init__()

        self.hlayout = QHBoxLayout()

        self.layerm = Layermodel()
        self.hlayout.addWidget(self.layerm)

        self.vw = ViewWidget()
        self.hlayout.addWidget(self.vw)
        self.vw.edge_btn.clicked.connect(self.showEdge)

        self.stackWidget = QStackedWidget()
        self.stackWidget.setFixedWidth(200)
        self.nothingWidget = QWidget()
        self.stackWidget.addWidget(self.nothingWidget)
        self.hlayout.addWidget(self.stackWidget)
        self.setLayout(self.hlayout)

        self.vw.gv.graphics_scene.show_attribute_signal.connect(
            self.showAttributeSignal)
        self.vw.gv.graphics_scene.add_attribute_signal.connect(
            self.addAttributeSignal)
        self.vw.gv.graphics_scene.remove_attribute_signal.connect(
            self.removeAttributeSignal)
        self.stackWidget.setCurrentIndex(0)

    def showAttributeSignal(self, i):
        self.stackWidget.setCurrentIndex(i+1)

    def addAttributeSignal(self, id):
        if id == 1:
            newAttrWidget = ConvWidget()
            i = len(self.attr_widget)
            self.attr_widget.append(newAttrWidget)
            self.stackWidget.addWidget(self.attr_widget[i])
        elif id == 2:
            newAttrWidget = MaxpoolWidget()
            i = len(self.attr_widget)
            self.attr_widget.append(newAttrWidget)
            self.stackWidget.addWidget(self.attr_widget[i])
        elif id == 3:
            newAttrWidget = FlatWidget()
            i = len(self.attr_widget)
            self.attr_widget.append(newAttrWidget)
            self.stackWidget.addWidget(self.attr_widget[i])
        elif id == 4:
            newAttrWidget = DenseWidget()
            i = len(self.attr_widget)
            self.attr_widget.append(newAttrWidget)
            self.stackWidget.addWidget(self.attr_widget[i])
        elif id == 5:
            newAttrWidget = InputWidget()
            i = len(self.attr_widget)
            self.attr_widget.append(newAttrWidget)
            self.stackWidget.addWidget(self.attr_widget[i])
        elif id == 6:
            newAttrWidget = OutputWidget()
            i = len(self.attr_widget)
            self.attr_widget.append(newAttrWidget)
            self.stackWidget.addWidget(self.attr_widget[i])

    def removeAttributeSignal(self, i):
        self.stackWidget.removeWidget(self.attr_widget[i])
        self.attr_widget.remove(self.attr_widget[i])
        self.stackWidget.setCurrentIndex(0)

    def showEdge(self):
        layer_json = "Json: \n"
        now_node = None
        gs = self.vw.gv.graphics_scene
        edge_label = self.vw.edgeLabel
        edge_label.setText("Edge: \n")
        for node in gs.nodes:
            if node.id == 5:
                now_node = node
        if now_node == None:
            print("No Input Layer")
            return

        for i in range(len(gs.nodes)):
            if now_node.id != 6 and now_node.rightPort.edge_index != -1:
                self.layer_index_order.append(now_node.index)
                edge_label.setText(edge_label.text() +
                                   "index: " + str(now_node.index) +
                                   ", id: " + str(now_node.id) +
                                   ", name: " + now_node.name +
                                   ", next edge's index: " + str(now_node.rightPort.edge_index)+"\n")
                now_node = gs.nodes[gs.edges[now_node.rightPort.edge_index].end_node.index]
            else:
                self.layer_index_order.append(now_node.index)
                edge_label.setText(edge_label.text() +
                                   "index: " + str(now_node.index) +
                                   ", id: " + str(now_node.id) +
                                   ", name: " + now_node.name +
                                   ", next edge's index: The End\n")
                break

        for i in self.layer_index_order:
            if self.attr_widget[i].id == 1:
                layer_json += ("{\"id\":" + str(self.attr_widget[i].id) +
                               ",\"filters\":\"" + str(self.attr_widget[i].convfilter.value()) +
                               "\",\"kernel_size\":\"" + str(self.attr_widget[i].convkernel_size.value()) +
                               "\",\"padding\":\"" + self.attr_widget[i].convpadding.currentText() +
                               "\",\"activation\":\"" + self.attr_widget[i].convactivation.currentText() + "\"}")
            elif self.attr_widget[i].id == 2:
                layer_json += ("{\"id\":" + str(self.attr_widget[i].id) +
                               ",\"pool_size\":\"" + str(self.attr_widget[i].poolpool_size.value()) + "\"}")
            elif self.attr_widget[i].id == 3:
                layer_json += ("{\"id\":" + str(self.attr_widget[i].id) + "}")
            elif self.attr_widget[i].id == 4:
                layer_json += ("{\"id\":" + str(self.attr_widget[i].id) +
                               ",\"units\":\"" + str(self.attr_widget[i].denseunits.value()) +
                               "\",\"activation\":\"" + self.attr_widget[i].denseactivation.currentText() + "\"}")
            elif self.attr_widget[i].id == 5:
                # layer_json += "{\"id\":" + str(self.attr_widget[i].id) + ","
                pass
            elif self.attr_widget[i].id == 6:
                # layer_json += "{\"id\":" + str(self.attr_widget[i].id) + ","
                pass

        edge_label.setText(edge_label.text() + layer_json)
        layer_json = "Json: \n"
        self.layer_index_order.clear()

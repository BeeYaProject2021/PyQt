import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class GraphicsView(QGraphicsView):

    start = None
    end = None
    item = None
    path = None
    layerWidget = []
    layerProxyWidget = []

    def __init__(self):
        super(GraphicsView, self).__init__()
        self.setAcceptDrops(True)
        self.setMouseTracking(True)

        self.setScene(QGraphicsScene())

        self.path = QPainterPath()
        self.item = GraphicsPathItem()

        self.scene().addItem(self.item)
        # self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        # self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        # self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

    def mousePressEvent(self, e):
        if e.buttons() == Qt.RightButton:
            self.start = self.mapToScene(e.pos())
            self.path.moveTo(self.start)
        super(GraphicsView, self).mousePressEvent(e)

    def mouseMoveEvent(self, e):
        if e.buttons() == Qt.RightButton:
            self.end = self.mapToScene(e.pos())
            self.path.lineTo(self.end)
            self.start = self.end
            self.item.setPath(self.path)
        super(GraphicsView, self).mouseMoveEvent(e)

    def dragEnterEvent(self, e):
        e.accept()

    def dragMoveEvent(self, e):
        if e.mimeData().text() == "widget":
            e.source().move((self.mapToScene(e.pos()) - e.source().epos).toPoint())
            e.accept()
        # print("move pos")
        # print(e.source().epos)

    def dropEvent(self, e):
        if e.mimeData().text() == "widget":
            e.source().move((self.mapToScene(e.pos()) - e.source().epos).toPoint())
            e.setDropAction(Qt.MoveAction)
            e.accept()
        elif e.mimeData().text() == "conv2D":
            e.accept()
            index = len(self.layerWidget)
            self.lw = WidgetA(index, 1)
            self.layerWidget.append(self.lw)
            self.lvlayout = QVBoxLayout()
            self.lvlayout.addStretch()
            self.lvlayout.addWidget(
                QLabel("index: "+str(self.layerWidget[index].index)))
            self.lvlayout.addWidget(
                QLabel("id: "+str(self.layerWidget[index].id)))
            self.lvlayout.addWidget(QPushButton("button"))
            self.lvlayout.addStretch()
            self.layerWidget[index].setLayout(self.lvlayout)
            self.layerWidget[index].move((self.mapToScene(e.pos())).toPoint())
            self.lw2 = QGraphicsProxyWidget()
            self.layerProxyWidget.append(self.lw2)
            self.layerProxyWidget[index].setWidget(self.layerWidget[index])
            self.scene().addItem(self.layerProxyWidget[index])
        elif e.mimeData().text() == "maxpooling2D":
            e.accept()
            index = len(self.layerWidget)
            self.lw = WidgetA(index, 2)
            self.layerWidget.append(self.lw)
            self.lvlayout = QVBoxLayout()
            self.lvlayout.addStretch()
            self.lvlayout.addWidget(
                QLabel("index: "+str(self.layerWidget[index].index)))
            self.lvlayout.addWidget(
                QLabel("id: "+str(self.layerWidget[index].id)))
            self.lvlayout.addWidget(QPushButton("button"))
            self.lvlayout.addStretch()
            self.layerWidget[index].setLayout(self.lvlayout)
            self.layerWidget[index].move((self.mapToScene(e.pos())).toPoint())
            self.lw2 = QGraphicsProxyWidget()
            self.layerProxyWidget.append(self.lw2)
            self.layerProxyWidget[index].setWidget(self.layerWidget[index])
            self.scene().addItem(self.layerProxyWidget[index])
        elif e.mimeData().text() == "flatten":
            e.accept()
            index = len(self.layerWidget)
            self.lw = WidgetA(index, 3)
            self.layerWidget.append(self.lw)
            self.lvlayout = QVBoxLayout()
            self.lvlayout.addStretch()
            self.lvlayout.addWidget(
                QLabel("index: "+str(self.layerWidget[index].index)))
            self.lvlayout.addWidget(
                QLabel("id: "+str(self.layerWidget[index].id)))
            self.lvlayout.addWidget(QPushButton("button"))
            self.lvlayout.addStretch()
            self.layerWidget[index].setLayout(self.lvlayout)
            self.layerWidget[index].move((self.mapToScene(e.pos())).toPoint())
            self.lw2 = QGraphicsProxyWidget()
            self.layerProxyWidget.append(self.lw2)
            self.layerProxyWidget[index].setWidget(self.layerWidget[index])
            self.scene().addItem(self.layerProxyWidget[index])
        elif e.mimeData().text() == "dense":
            e.accept()
            index = len(self.layerWidget)
            self.lw = WidgetA(index, 4)
            self.layerWidget.append(self.lw)
            self.lvlayout = QVBoxLayout()
            self.lvlayout.addStretch()
            self.lvlayout.addWidget(
                QLabel("index: "+str(self.layerWidget[index].index)))
            self.lvlayout.addWidget(
                QLabel("id: "+str(self.layerWidget[index].id)))
            self.lvlayout.addWidget(QPushButton("button"))
            self.lvlayout.addStretch()
            self.layerWidget[index].setLayout(self.lvlayout)
            self.layerWidget[index].move((self.mapToScene(e.pos())).toPoint())
            self.lw2 = QGraphicsProxyWidget()
            self.layerProxyWidget.append(self.lw2)
            self.layerProxyWidget[index].setWidget(self.layerWidget[index])
            self.scene().addItem(self.layerProxyWidget[index])


class GraphicsPathItem(QGraphicsPathItem):

    def __init__(self):
        super(GraphicsPathItem, self).__init__()
        pen = QPen()
        pen.setColor(Qt.black)
        pen.setWidth(10)
        self.setPen(pen)


class WidgetA(QWidget):
    epos = QPoint()

    def __init__(self, index, id):
        super(WidgetA, self).__init__()
        self.index = index
        self.id = id
        self.setMouseTracking(True)
        self.resize(200, 100)

    def mouseMoveEvent(self, e):
        if e.buttons() != Qt.LeftButton:
            return

        mimeData = QMimeData()
        mimeData.setText("widget")
        print(e.pos())
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())
        self.epos = e.pos()
        dropAction = drag.exec_(Qt.MoveAction)
        print(self.epos)
        print("YES")

    def mousePressEvent(self, e):

        if e.button() == Qt.LeftButton:
            x = 0
            # print('press')


class ViewWidget(QWidget):

    central_widget = None
    layout_container = None

    def __init__(self):
        super(ViewWidget, self).__init__()
        # self.central_widget = QWidget()
        self.vlayout = QVBoxLayout()
        self.setLayout(self.vlayout)
        # self.setCentralWidget(self.central_widget)
        self.gv = GraphicsView()
        self.vlayout.addWidget(self.gv)
        self.toggle_btn = QPushButton("Toggle Drag Mode")
        self.toggle_btn.clicked.connect(self.toggle_drag_mode)
        self.vlayout.addWidget(self.toggle_btn)
        self.resize(1280, 720)

    def toggle_drag_mode(self):
        if self.gv.dragMode() == QGraphicsView.ScrollHandDrag:
            self.gv.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        else:
            self.gv.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)

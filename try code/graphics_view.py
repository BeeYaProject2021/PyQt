import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class MainWindow(QMainWindow):

    central_widget = None
    layout_container = None

    def __init__(self):
        super(MainWindow, self).__init__()
        self.central_widget = QWidget()
        self.layout_container = QVBoxLayout()
        self.central_widget.setLayout(self.layout_container)
        self.setCentralWidget(self.central_widget)
        self.gv = GraphicsView()
        self.layout_container.addWidget(self.gv)
        self.resize(1280, 720)


class GraphicsView(QGraphicsView):

    start = None
    end = None
    item = None
    path = None

    def __init__(self):
        super(GraphicsView, self).__init__()
        self.setScene(QGraphicsScene())
        self.path = QPainterPath()
        self.item = GraphicsPathItem()

        for i in range(10):
            self.photo = QtWidgets.QGraphicsPixmapItem()
            self.photo.setPixmap(QtGui.QPixmap('image.jpg'))
            self.photo.setPos(400*i, 0)
            self.scene().addItem(self.photo)
        # self.photo = QtWidgets.QGraphicsPixmapItem()
        # self.photo.setPixmap(QtGui.QPixmap('image.jpg'))
        # self.photo2 = QtWidgets.QGraphicsPixmapItem()
        # self.photo2.setPixmap(QtGui.QPixmap('image.jpg'))
        # self.photo2.setPos(400, 0)
        # self.scene().addItem(self.photo)
        # self.scene().addItem(self.photo2)
        self.scene().addItem(self.item)
        # self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        # self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            factor = 1.25
        else:
            factor = 0.8

        self.scale(factor, factor)

    def mousePressEvent(self, event):

        self.start = self.mapToScene(event.pos())
        self.path.moveTo(self.start)
        super(GraphicsView, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.RightButton:
            self.end = self.mapToScene(event.pos())
            self.path.lineTo(self.end)
            self.start = self.end
            self.item.setPath(self.path)
        super(GraphicsView, self).mouseMoveEvent(event)


class GraphicsPathItem(QGraphicsPathItem):

    def __init__(self):
        super(GraphicsPathItem, self).__init__()
        pen = QPen()
        pen.setColor(Qt.black)
        pen.setWidth(10)
        self.setPen(pen)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())

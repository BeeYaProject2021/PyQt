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

    def __init__(self):
        super(GraphicsView, self).__init__()
        self.setAcceptDrops(True)
        self.setMouseTracking(True)

        self.setScene(QGraphicsScene())
        self.path = QPainterPath()
        self.item = GraphicsPathItem()
        self.gw = WidgetA()
        self.vlayout = QVBoxLayout()
        self.vlayout.addWidget(QPushButton("button"))
        self.gw.setLayout(self.vlayout)
        # self.gw.setWidget(QPushButton("button"))
        self.widget = QWidget()
        self.gw2 = QGraphicsProxyWidget()
        # self.gw2.setWidget(self.widget)
        self.gw2.setWidget(self.gw)
        # self.btn = Button("BButton", self)
        # self.gw2.setWidget(self.btn)

        for i in range(10):
            self.photo = QtWidgets.QGraphicsPixmapItem()
            self.photo.setPixmap(QtGui.QPixmap('image.jpg'))
            self.photo.setPos(400*i, 0)
            self.scene().addItem(self.photo)

        # self.scene().addItem(self.gw)
        self.scene().addItem(self.gw2)
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
        e.source().move((self.mapToScene(e.pos()) - e.source().epos).toPoint())
        e.accept()
        print("move pos")
        print(e.source().epos)

    def dropEvent(self, e):
        e.source().move((self.mapToScene(e.pos()) - e.source().epos).toPoint())
        print("view pos")
        print(e.pos())
        e.setDropAction(Qt.MoveAction)
        e.accept()


class GraphicsPathItem(QGraphicsPathItem):

    def __init__(self):
        super(GraphicsPathItem, self).__init__()
        pen = QPen()
        pen.setColor(Qt.black)
        pen.setWidth(10)
        self.setPen(pen)


class WidgetA(QWidget):
    epos = QPoint()

    def __init__(self):
        super(WidgetA, self).__init__()
        self.setMouseTracking(True)
        self.resize(400, 400)

    def mouseMoveEvent(self, e):
        if e.buttons() != Qt.LeftButton:
            return

        mimeData = QMimeData()
        mimeData.setText("HI")
        print(e.pos())
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())
        # drag.setHotSpot(e.pos()+self.pos())
        self.epos = e.pos()
        dropAction = drag.exec_(Qt.MoveAction)
        print(self.epos)
        print("YES")

    def mousePressEvent(self, e):

        if e.button() == Qt.LeftButton:
            x = 0
            # print('press')


class MainWindow(QMainWindow):

    central_widget = None
    layout_container = None

    def __init__(self):
        super(MainWindow, self).__init__()
        self.central_widget = QWidget()
        self.vlayout = QVBoxLayout()
        self.central_widget.setLayout(self.vlayout)
        self.setCentralWidget(self.central_widget)
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())

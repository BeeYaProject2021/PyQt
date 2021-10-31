from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag


class Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.view = View(self)
        self.button = QPushButton('Clear View', self)
        self.button.clicked.connect(self.handleClearView)
        layout = QVBoxLayout(self)
        layout.addWidget(self.view)
        layout.addWidget(self.button)


    def handleClearView(self):
        self.view.scene().clear()


class DragButton(QPushButton):
    def __init__(self, title, parent=None):
        super().__init__(title, parent)

    def mouseMoveEvent(self, e):

        if e.buttons() != Qt.LeftButton:
            return

        mimeData = QMimeData()
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())
        dropAction = drag.exec_(Qt.MoveAction)


class View(QGraphicsView):
    def __init__(self, parent):
        QGraphicsView.__init__(self, parent)
        self.setScene(QGraphicsScene(self))
        self.setAcceptDrops(True)
        self.setSceneRect(QtCore.QRectF(self.viewport().rect()))
        self.btn1=DragButton('Test1', self)
        self.btn2=DragButton('Test2', self)

    def clearScene(self):
        self.scene().clear()

    def dragEnterEvent(self, e):
        if e.source() in [self.btn1, self.btn2]:
            self.clearScene()
        e.accept()

    def dragMoveEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        btn = e.source()
        otherBtn = self.btn2 if btn == self.btn1 else self.btn1
        position = e.pos()
        btn.move(position)

        start = QtCore.QPointF(self.mapToScene(btn.pos()))
        end = QtCore.QPointF(self.mapToScene(otherBtn.pos()))

        self.scene().addItem(
            QGraphicsLineItem(QtCore.QLineF(start, end)))

        e.setDropAction(Qt.MoveAction)
        e.accept()


if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    window = Window()
    window.resize(640, 480)
    window.show()
    sys.exit(app.exec_())
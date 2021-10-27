import sys

from PyQt5.QtCore import QPoint, Qt, QMimeData
from PyQt5.QtGui import QDrag
from PyQt5.QtWidgets import QLabel, QPushButton, QWidget, QApplication


class Button(QLabel):

    epos = QPoint()

    def __init__(self, title, parent):
        super().__init__(title, parent)

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


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.setAcceptDrops(True)

        self.button = Button('Button', self)
        self.button.move(100, 65)

        self.setWindowTitle('Click or Move')
        self.setGeometry(300, 300, 550, 450)

    def dragEnterEvent(self, e):
        e.accept()

    def dragMoveEvent(self, e):
        self.button.move(e.pos() - self.button.epos)
        e.accept()

    def dropEvent(self, e):
        self.button.move(e.pos() - self.button.epos)

        e.setDropAction(Qt.MoveAction)
        e.accept()


def main():

    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    app.exec_()


if __name__ == '__main__':
    main()

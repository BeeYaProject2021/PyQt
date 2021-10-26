from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from page2 import *
from page_input import *

import os
import sys


class TabBar(QTabBar):
    def tabSizeHint(self, index):
        size = QTabBar.tabSizeHint(self, index)
        w = int(self.width()/self.count())
        print(self.width())
        return QSize(w, size.height())


class Button(QPushButton):

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


class WidgetA(QWidget):

    def __init__(self, parent):
        super(WidgetA, self).__init__(parent)

        self.initUI()

    def initUI(self):

        self.setAcceptDrops(True)

        self.button = Button('Button', self)
        self.button.move(100, 65)

        self.button2 = Button('Button2', self)
        self.button2.move(100, 165)

    def dragEnterEvent(self, e):
        e.accept()

    def dragMoveEvent(self, e):
        e.source().move(e.pos() - e.source().epos)
        e.accept()

    def dropEvent(self, e):
        e.source().move(e.pos() - e.source().epos)
        e.setDropAction(Qt.MoveAction)
        e.accept()


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.tabs = QTabWidget()
        self.tb = TabBar()
        # label = "Blank"
        # a = WidgetA(self)
        # i = self.tb.addTab(label)
        # self.tb.setCurrentIndex(i)
        # self.tabs.setTabBar(self.tb)

        # self.tabs.setStyleSheet(
        #     "QTabBar::tab::first { height: 100px; width: 100px; background: 'red'}")
        label = "Dataset"
        a = InputWidget()
        i = self.tabs.addTab(a, label)
        self.tabs.setCurrentIndex(i)
        label = "Model"
        b = initialWidget()
        i = self.tabs.addTab(b, label)
        label = "Blank1.5"
        c = WidgetA(self)
        i = self.tabs.addTab(c, label)
        label = "Blank2"
        c = WidgetA(self)
        i = self.tabs.addTab(c, label)

        # self.tabs.setDocumentMode(True)
        # self.tabs.currentChanged.connect(self.current_tab_changed)

        self.setCentralWidget(self.tabs)

        self.resize(1280, 720)

        self.show()


app = QApplication(sys.argv)

window = MainWindow()

app.exec_()

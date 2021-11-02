from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from page_setting import *
from page_model import *
from page_input import *
from page_training import *

import os
import sys

StyleSheet = '''
QTabBar::tab {
    border: 2px solid #E0E0E0;
    border-bottom-color: #E0E0E0; /* same as the pane color */
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    min-width: 20ex;
    padding: 2px;
}
QTabBar::tab:selected, QTabBar::tab:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #fafafa, stop: 0.4 #f4f4f4, stop: 0.5 #e7e7e7, stop: 1.0 #fafafa);
}
QTabBar::tab:selected {
    border-color: #9B9B9B;
    border-bottom-color: #9B9B9B; /* same as pane color */
}
QTabBar::tab:!selected {
    margin-top: 2px; /* make non-selected tabs look smaller */
}
/* make use of negative margins for overlapping tabs */
QTabBar::tab:selected {
    /* expand/overlap to the left and right by 4px */
    margin-left: -4px;
    margin-right: -4px;
}
QTabBar::tab:first:selected {
    margin-left: 0; /* the first selected tab has nothing to overlap with on the left */
}
QTabBar::tab:last:selected {
    margin-right: 0; /* the last selected tab has nothing to overlap with on the right */
}
QTabBar::tab:only-one {
    margin: 0; /* if there is only one tab, we don't want overlapping margins */
}
'''


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
        self.inputW = InputWidget()
        i = self.tabs.addTab(self.inputW, label)
        self.inputW.img_total_signal.connect(self.img_signal_acc)

        label = "Model"
        self.modelW = ModelWidget()
        i = self.tabs.addTab(self.modelW, label)
        label = "Blank1.5"
        self.settingW = SettingWidget()
        self.settingW.batch_epoch_signal.connect(self.batch_epoch_signal_acc)
        i = self.tabs.addTab(self.settingW, label)
        label = "Blank2"
        self.trainingW = TrainingWidget()
        i = self.tabs.addTab(self.trainingW, label)
        self.tabs.setCurrentIndex(1)
        # self.tabs.setDocumentMode(True)
        # self.tabs.currentChanged.connect(self.current_tab_changed)
        self.setStyleSheet(StyleSheet)
        self.setCentralWidget(self.tabs)
        self.resize(1280, 720)
        self.show()

    def img_signal_acc(self, msg):
        self.trainingW.img_total = msg

    def batch_epoch_signal_acc(self, batch, epoch):
        self.trainingW.batch_size = batch
        self.trainingW.epoch = epoch


app = QApplication(sys.argv)

window = MainWindow()

app.exec_()

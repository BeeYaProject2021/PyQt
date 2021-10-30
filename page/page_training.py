from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import QThread, QTimer, Qt, pyqtSignal
import time
import pyqtgraph as pg
import sys
import os
from random import randint
from pyqtgraph import PlotWidget, plot

# now_i = 0


class Thread(QThread):
    _signal = pyqtSignal(int)

    def __init__(self):
        super(Thread, self).__init__()

    def run(self):
        max_value = 100
        for i in range(max_value+1):
            time.sleep(0.2)
            self._signal.emit(i)


class trainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(1000, 650)
        self.graphWidget = pg.PlotWidget(self)
        # self.setCentralWidget(self.graphWidget)
        self.graphWidget.resize(600, 350)
        self.graphWidget.move(10, 50)
        self.x = list(range(100))  # 100 time points
        self.y = [randint(0, 100) for _ in range(100)]  # 100 data points

        self.step = 0

        self.graphWidget.setBackground('w')

        pen = pg.mkPen(color=(255, 0, 0))
        self.data_line = self.graphWidget.plot(self.x, self.y, pen=pen)
        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

        # _translate = QtCore.QCoreApplication.translate
        self.pushButton_1 = QtWidgets.QPushButton(self)
        self.pushButton_1.setGeometry(QtCore.QRect(710, 10, 35, 35))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("./image/rotate-left 4.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_1.setIcon(icon1)

        self.pushButton_2 = QtWidgets.QPushButton(self)
        self.pushButton_2.setGeometry(QtCore.QRect(760, 10, 35, 35))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("./image/rotate-right 2.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_2.setIcon(icon2)

        self.pushButton_3 = QtWidgets.QPushButton(self)
        self.pushButton_3.setGeometry(QtCore.QRect(810, 10, 35, 35))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("./image/4_audio_play.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_3.setIcon(icon3)

        self.pushButton_4 = QtWidgets.QPushButton(self)
        self.pushButton_4.setGeometry(QtCore.QRect(860, 10, 35, 35))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("./image/4_audio_stop.ico"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_4.setIcon(icon4)

        self.pushButton_5 = QtWidgets.QPushButton(self)
        self.pushButton_5.setGeometry(QtCore.QRect(910, 10, 35, 35))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("./image/4_audio_pause.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_5.setIcon(icon5)

        self.toolButton_4 = QtWidgets.QToolButton(self)
        self.toolButton_4.setGeometry(QtCore.QRect(600, 10, 35, 35))
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("./image/screenshot.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_4.setIcon(icon6)

        self.toolButton_5 = QtWidgets.QToolButton(self)
        self.toolButton_5.setGeometry(QtCore.QRect(650, 10, 35, 35))
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("./image/save.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_5.setIcon(icon7)

        self.progressBar = QtWidgets.QProgressBar(self)
        self.progressBar.setGeometry(QtCore.QRect(370, 480, 273, 16))

        self.pushButtongo = QPushButton("GO", self)
        self.pushButtongo.setGeometry(QtCore.QRect(700, 470, 35, 31))
        # self.pushButtongo.setText(_translate("MainWindow", "go"))

        self.pushButtongo.clicked.connect(self.start_progress)

        # self.v_layout = QVBoxLayout()
        # self.v_layout.addWidget(self.progressBar)
        # self.v_layout.addWidget(self.pushButtongo)

        # self.setLayout(self.v_layout)

        # self.timer = time.sleep(0.2)

    def update_plot_data(self):

        self.x = self.x[1:]  # Remove the first y element.
        # Add a new value 1 higher than the last.
        self.x.append(self.x[-1] + 1)

        self.y = self.y[1:]  # Remove the first
        self.y.append(randint(0, 100))  # Add a new random value.

        self.data_line.setData(self.x, self.y)  # Update the data.

    def start_progress(self):

        self.thread = Thread()
        self.thread._signal.connect(self.signal_accept)
        self.thread.start()
        self.pushButtongo.setEnabled(False)

    # def update_func(self):
    #     self.step += 1
    #     self.progressBar(str(self.step))

    def signal_accept(self, msg):
        self.progressBar.setValue(int(msg))
        if self.progressBar.value() >= 100:
            self.pushButtongo.setEnabled(True)


# if __name__ == '__main__':

#     import sys

#     app = QApplication(sys.argv)
#     mw = trainWidget()
#     mw.show()
#     sys.exit(app.exec_())

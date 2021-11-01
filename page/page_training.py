from re import S
import time
import sys
import os
import socket
import pyqtgraph as pg
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import QThread, QTimer, Qt, pyqtSignal
from random import randint
from pyqtgraph import PlotWidget, plot


class Thread(QThread):
    _signal = pyqtSignal(int)
    accuracy_signal = pyqtSignal(int, float)

    def __init__(self):
        super(Thread, self).__init__()

    def run(self):
        ClientSocket = socket.socket()
        ClientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        host = '140.136.151.88'
        port = 48763

        print('Waiting for backend connection')

        connected = False
        while not connected:
            try:
                ClientSocket.connect((host, port))
                connected = True
            except Exception as e:
                pass  # Do nothing, just try again

        batch_cnt = 0
        epoch_cnt = 0
        while True:
            Response = ClientSocket.recv(67)
            strRes = Response.decode('utf-8')
            print(strRes)

            self._signal.emit(batch_cnt)
            if '@' in strRes:
                data = strRes.split('@')
                print(data[1], data[2], data[3])
                batch_cnt += 1
                self.accuracy_signal.emit(batch_cnt, float(data[2]))
            if '#' in strRes:
                data = strRes.split('#')
                print(data[1], data[2], data[3])
                # epoch_cnt += 1
                # self.accuracy_signal.emit(data[2])

            if 'over' in strRes:
                break

        ClientSocket.close()


class TrainingWidget(QWidget):
    img_total = 0
    batch_size = 0
    epoch = 0

    def __init__(self):
        super().__init__()
        self.resize(1000, 650)
        self.graphWidget = pg.PlotWidget(self)
        self.graphWidget.resize(600, 350)
        self.graphWidget.move(10, 50)
        self.graphWidget.showGrid(x=True, y=True)
        self.graphWidget.addLegend()
        self.accuracy_x = []
        self.accuracy_y = []
        self.val_accuracy_x = []
        self.val_accuracy_y = []

        # self.step = 0

        self.graphWidget.setBackground('w')

        training_pen = pg.mkPen(color=(255, 0, 0))
        validation_pen = pg.mkPen(color=(0, 0, 255))
        self.training_line = self.graphWidget.plot(
            self.accuracy_x, self.accuracy_y, pen=training_pen, name='Training')
        self.training_line = self.graphWidget.plot(
            self.val_accuracy_x, self.val_accuracy_y, pen=validation_pen, name='Validation')

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

    def start_progress(self):
        # Maximum = image/batch_size x epochs
        print(str(self.img_total)+" "+str(self.batch_size)+" "+str(self.epoch))
        self.progressBar.setValue(0)
        self.accuracy_x.clear()
        self.accuracy_y.clear()
        self.training_line.setData(self.accuracy_x, self.accuracy_y)
        if self.img_total > 0 and self.batch_size > 0 and self.epoch > 0:
            print("GOOOOO")
            self.progressBar.setMaximum(
                (self.img_total/self.batch_size)*self.epoch)
            self.thread = Thread()
            self.thread._signal.connect(self.signal_accept)
            self.thread.accuracy_signal.connect(self.update_plot_data)
            self.thread.start()
            self.pushButtongo.setEnabled(False)

    def signal_accept(self, msg):
        self.progressBar.setValue(int(msg))
        if self.progressBar.value() == 100:
            self.pushButtongo.setEnabled(True)

    def update_plot_data(self, x, y):
        self.accuracy_x.append(x)
        self.accuracy_y.append(y)
        self.training_line.setData(self.accuracy_x, self.accuracy_y)

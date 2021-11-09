# from _typeshed import Self
from re import S
import time
import sys
import os
import socket
import pyqtgraph as pg
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QHBoxLayout, QMainWindow, QFileDialog, QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import QThread, QTimer, Qt, pyqtSignal
from random import randint
from pyqtgraph import PlotWidget, plot
from screenshot import *


class Thread(QThread):
    # Setup signal for thread
    _signal = pyqtSignal(int)
    accuracy_signal = pyqtSignal(int, float)
    val_accuracy_signal = pyqtSignal(int, float)
    loss_signal = pyqtSignal(int, float)
    val_loss_signal = pyqtSignal(int, float)

    def __init__(self):
        super(Thread, self).__init__()

    def run(self):
        ClientSocket = socket.socket()
        ClientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        host = '140.136.204.132'
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
            # Response = ClientSocket.recv(67)
            Response = ClientSocket.recv(1024)
            strRes = Response.decode('utf-8')
            print(strRes)
            lines=strRes.split('\r\n')

            over = False
            for line in lines:
                self._signal.emit(batch_cnt)
                if '@' in line:
                    data = line.split('@')
                    print(data[1], data[2], data[3])
                    batch_cnt += 1

                    # Use signal to inform the thread run function
                    # Emit the batch_size as x-axis and accuracy, loss as y-axis
                    self.accuracy_signal.emit(batch_cnt, float(data[2]))
                    self.loss_signal.emit(batch_cnt, float(data[3]))

                if '#' in line:
                    data = line.split('#')
                    print(data[1], data[2], data[3], data[4], data[5])
                    epoch_cnt += 1

                    self.val_accuracy_signal.emit(batch_cnt, float(data[3]))
                    self.val_loss_signal.emit(batch_cnt, float(data[5]))

                if 'over' in line:
                    over = True
                    ClientSocket.close()
                    break

            if over == True:
                break

class screen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = CaptureScreen()
        # self.ui.setupUi(self)


class TrainingWidget(QWidget):
    img_total = 0
    batch_size = 0
    epoch = 0

    def __init__(self):
        super().__init__()

        self.vtrainw = QVBoxLayout()

        self.buttonlayout  = QHBoxLayout()
        self.buttonlayout.addStretch(2)

        self.pushButton_1 = QtWidgets.QPushButton(self)
        self.pushButton_1.resize(50, 50)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("./image/rotate-left 4.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_1.setIcon(icon1)
        self.buttonlayout.addWidget(self.pushButton_1)

        self.pushButton_2 = QtWidgets.QPushButton(self)
        self.pushButton_2.resize(50, 50)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("./image/rotate-right 2.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_2.setIcon(icon2)
        self.buttonlayout.addWidget(self.pushButton_2)

        self.pushButton_3 = QtWidgets.QPushButton(self)
        self.pushButton_3.resize(50, 50)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("./image/4_audio_play.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_3.setIcon(icon3)
        self.buttonlayout.addWidget(self.pushButton_3)

        self.pushButton_4 = QtWidgets.QPushButton(self)
        self.pushButton_4.resize(50, 50)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("./image/4_audio_stop.ico"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_4.setIcon(icon4)
        self.buttonlayout.addWidget(self.pushButton_4)

        self.pushButton_5 = QtWidgets.QPushButton(self)
        self.pushButton_5.resize(50, 50)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("./image/4_audio_pause.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_5.setIcon(icon5)
        self.buttonlayout.addWidget(self.pushButton_5)
        self.buttonlayout.addStretch(2)

        self.toolButton_4 = QtWidgets.QToolButton(self)
        self.toolButton_4.resize(50, 50)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("./image/screenshot.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_4.setIcon(icon6)
        self.buttonlayout.addWidget(self.toolButton_4)

        self.toolButton_5 = QtWidgets.QToolButton(self)
        self.toolButton_5.resize(50, 50)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("./image/save.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_5.setIcon(icon7)
        self.buttonlayout.addWidget(self.toolButton_5)

        self.buttonlayout.addStretch(2)
        self.vtrainw.addLayout(self.buttonlayout)

        # self.vtrainw.addStretch()
        self.graphlayout = QHBoxLayout()

        self.graphWidget = pg.PlotWidget(self)
        self.graphWidget.resize(600, 350)
        self.graphlayout.addWidget(self.graphWidget)
        # self.graphWidget.move(10, 50)
        self.graphWidget.showGrid(x=True, y=True)
        self.graphWidget.addLegend()
        self.accuracy_x = []
        self.accuracy_y = []
        self.val_accuracy_x = []
        self.val_accuracy_y = []

        self.graphWidget.setBackground('w')

        training_pen = pg.mkPen(color=(255, 0, 0))
        validation_pen = pg.mkPen(color=(0, 0, 255))
        self.training_line = self.graphWidget.plot(
            self.accuracy_x, self.accuracy_y, pen=training_pen, name='Training')
        self.validation_line = self.graphWidget.plot(
            self.val_accuracy_x, self.val_accuracy_y, pen=validation_pen, name='Validation')

        self.lossWidget = pg.PlotWidget(self)
        self.lossWidget.resize(600, 350)
        self.graphlayout.addWidget(self.lossWidget)
        # self.lossWidget.move(650, 50)
        self.lossWidget.showGrid(x=True, y=True)
        self.lossWidget.addLegend()

        self.loss_x = []
        self.loss_y = []
        self.val_loss_x = []
        self.val_loss_y = []

        self.lossWidget.setBackground('w')

        training_pen = pg.mkPen(color=(255, 0, 0))
        validation_pen = pg.mkPen(color=(0, 0, 255))
        self.training_loss_line = self.lossWidget.plot(
            self.loss_x, self.loss_y, pen=training_pen, name='Loss')
        self.validation_loss_line = self.lossWidget.plot(
            self.val_loss_x, self.val_loss_y, pen=validation_pen, name='Validation_Loss')

        self.vtrainw.addLayout(self.graphlayout)

        self.vtrainw.addStretch()
        self.progresslayout = QHBoxLayout()
        self.progresslayout.addStretch()

        self.progressBar = QtWidgets.QProgressBar(self)
        self.progresslayout.addWidget(self.progressBar)
        # self.progressBar.setGeometry(QtCore.QRect(370, 470, 270, 30))


        self.pushButtongo = QPushButton("GO", self)
        self.progresslayout.addWidget(self.pushButtongo)
        # self.pushButtongo.setGeometry(QtCore.QRect(700, 470, 35, 30))
        # self.pushButtongo.setText(_translate("MainWindow", "go"))

        self.progresslayout.addStretch()

        with open("./stylesheet/train.qss", "r") as f:    
            self.setStyleSheet(f.read())

        self.pushButtongo.clicked.connect(self.start_progress)

        self.vtrainw.addLayout(self.progresslayout)
        self.setLayout(self.vtrainw)

        # self.v_layout = QVBoxLayout()
        # self.v_layout.addWidget(self.progressBar)
        # self.v_layout.addWidget(self.pushButtongo)

        # self.setLayout(self.v_layout)

        # self.timer = time.sleep(0.2)

        self.cutscerrn = screen()
        self.toolButton_4.clicked.connect(self.cutscerrn.show)


    def start_progress(self):
        # Maximum = image/batch_size x epochs
        print(str(self.img_total)+" "+str(self.batch_size)+" "+str(self.epoch))

        self.progressBar.setValue(0)
        self.accuracy_x.clear()
        self.accuracy_y.clear()
        self.val_accuracy_x.clear()
        self.val_accuracy_y.clear()
        self.loss_x.clear()
        self.loss_y.clear()
        self.val_loss_x.clear()
        self.val_loss_y.clear()

        # Setup list x, y data
        self.training_line.setData(self.accuracy_x, self.accuracy_y)
        self.validation_line.setData(self.val_accuracy_x, self.val_accuracy_y)
        self.training_loss_line.setData(self.loss_x, self.loss_y)
        self.validation_loss_line.setData(self.val_loss_x, self.val_loss_y)

        if self.img_total > 0 and self.batch_size > 0 and self.epoch > 0:
            print("GOOOOO")
            self.progressBar.setMaximum(
                (self.img_total/self.batch_size)*self.epoch)

            # Thread for progressBar and data graph
            self.thread = Thread()
            self.thread._signal.connect(self.signal_accept)
            self.thread.accuracy_signal.connect(self.update_acc)
            self.thread.val_accuracy_signal.connect(self.update_val_acc)
            self.thread.loss_signal.connect(self.update_loss)
            self.thread.val_accuracy_signal.connect(self.update_val_loss)

            self.thread.start()
            self.pushButtongo.setEnabled(False)

    def signal_accept(self, msg):
        self.progressBar.setValue(int(msg))
        if self.progressBar.value() == self.progressBar.maximum():
            self.pushButtongo.setEnabled(True)

    def update_acc(self, x, y):
        self.accuracy_x.append(x)
        self.accuracy_y.append(y)
        self.training_line.setData(self.accuracy_x, self.accuracy_y)

    def update_val_acc(self, x, y):
        self.val_accuracy_x.append(x)
        self.val_accuracy_y.append(y)
        self.validation_line.setData(self.val_accuracy_x, self.val_accuracy_y)

    def update_loss(self, x, y):
        self.loss_x.append(x)
        self.loss_y.append(y)
        self.training_loss_line.setData(self.loss_x, self.loss_y)

    def update_val_loss(self, x, y):
        self.val_loss_x.append(x)
        self.val_loss_y.append(y)
        self.validation_loss_line.setData(self.val_loss_x, self.val_loss_y)
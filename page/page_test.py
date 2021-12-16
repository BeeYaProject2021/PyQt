from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import pathlib
import requests
import re
import socket
import page_training
import page_input
import page_model
import numpy as np
import matplotlib.pyplot as plt
from PIL.ImageQt import ImageQt
import tensorflow as tf


class Thread(QThread):

    response_signal = pyqtSignal(float, float)
    error_signal = pyqtSignal(str)
    guess_signal = pyqtSignal(int)

    def __init__(self, uid, batch, folder_path):
        super(Thread, self).__init__()
        self.uid = uid
        self.batch = batch
        self.path = folder_path

    def run(self):
        uid = self.uid
        batch = self.batch
        path = self.path

        url = 'http://140.136.204.132:8000/test/'
        x = requests.post(url, data={'uid': uid, 'batch': batch},
                          files={'file': open(path, 'rb')})
        # print(x.text)
        data = re.split(" |\"", x.text)
        print("response data", data)

        ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ClientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_OOBINLINE, 1)
        host = '140.136.204.132'
        port = (int)(data[2])

        print('Waiting for backend connection')
        connected = False
        while not connected:
            try:
                ClientSocket.connect((host, port))
                connected = True
            except Exception as e:
                pass  # Do nothing, just try again

        Response = ClientSocket.recv(1024)
        strRes = Response.decode('utf-8')
        data = strRes.split('#')

        if 'error' in strRes:
            self.error_signal.emit(strRes)
        else:
            loss, acc = data[1], data[2]
            print(loss, acc)
            self.response_signal.emit(float(loss), float(acc))

            g_cnt = 0
            while True:
                Response = ClientSocket.recv(1024)
                strRes = Response.decode('utf-8')
                lines = strRes.split('\r\n')

                over = False
                for i in lines:
                    # print(i)
                    if 'over' in i:
                        over = True
                        ClientSocket.close()
                        break
                    if i == '':
                        continue
                    self.guess_signal.emit(int(i))
                    g_cnt += 1

                if over == True:
                    break
            print("guess count: ", g_cnt)


class Thread2(QThread):

    error_signal2 = pyqtSignal(str)
    response_signal2 = pyqtSignal(int, float)

    def __init__(self, uid, h, w, c, folder_path):
        super(Thread2, self).__init__()
        self.uid = uid
        self.img_h = h
        self.img_w = w
        self.img_c = c
        self.path = folder_path

    def run(self):
        uid = self.uid
        h = self.img_h
        w = self.img_w
        c = self.img_c
        path = self.path

        url = 'http://140.136.204.132:8000/test/'
        x = requests.post(url, data={'uid': uid, 'img_h': h, 'img_w': w, 'img_c': c},
                          files={'file': open(path, 'rb')})

        data = re.split(" |\"", x.text)
        print("response data", data)

        ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ClientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_OOBINLINE, 1)
        host = '140.136.204.132'
        port = (int)(data[2])

        print('Waiting for backend connection')
        connected = False
        while not connected:
            try:
                ClientSocket.connect((host, port))
                connected = True
            except Exception as e:
                pass  # Do nothing, just try again

        Response = ClientSocket.recv(1024)
        strRes = Response.decode('utf-8')
        data = strRes.split('#')

        if 'error' in strRes:
            self.error_signal2.emit(strRes)
        else:
            guess, probability = data[1], data[2]
            print(guess, probability)
            self.response_signal2.emit(int(guess), float(probability))
            ClientSocket.close()


class TimgWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super(TimgWidget, self).__init__(*args, **kwargs)

        self.vlayout = QVBoxLayout()
        self.vlayout.addStretch()

        self.fileToggle = QPushButton("Toggle File")
        # self.fileToggle.setFixedWidth(150)

        self.vlayout.addWidget(self.fileToggle)

        self.filePathEdit = QLabel()
        self.filePathEdit.setObjectName("Path")
        self.filePathEdit.setFixedWidth(500)
        self.vlayout.addWidget(self.filePathEdit)

        self.hlayout = QHBoxLayout()
        self.ChooseFileBtn = QPushButton('NPZ')
        self.ChooseFileBtn.setFixedWidth(150)
        self.ChooseImgBtn = QPushButton('IMG')
        self.ChooseImgBtn.setFixedWidth(150)
        self.ChooseImgBtn.setVisible(False)

        self.hlayout.addWidget(self.ChooseFileBtn)
        self.hlayout.addWidget(self.ChooseImgBtn)

        self.batchlabel = QLabel("Batch size: ")
        self.batchlabel.setFont(QFont("Consolas", 15))
        self.hlayout.addWidget(self.batchlabel)
        self.batchBox = QSpinBox()
        self.batchBox.setRange(1, 100000)
        self.batchBox.setFixedWidth(150)
        self.hlayout.addWidget(self.batchBox)

        self.vlayout.addLayout(self.hlayout)
        self.vlayout.addStretch()
        self.setLayout(self.vlayout)


class Tbatch(QWidget):
    def __init__(self, *args, **kwargs):
        super(Tbatch, self).__init__(*args, **kwargs)

        self.vlayout = QVBoxLayout()
        self.vlayout.addStretch()

        self.imgshow = QLabel("Your Image: ")
        self.imgshow.setFont(QFont("Consolas", 15))
        # self.imgshow.setVisible(False)
        self.vlayout.addWidget(self.imgshow)

        self.imglabel = QLabel()
        self.imglabel.setObjectName("Path")
        # self.imglabel.setFixedSize(100, 100)
        self.imglabel.setScaledContents(True)
        # self.imglabel.setVisible(False)
        self.vlayout.addWidget(self.imglabel)

        self.guesslabel = QLabel("Predict: ")
        self.guesslabel.setFont(QFont("Consolas", 15))
        self.guesslabel.setVisible(False)
        self.vlayout.addWidget(self.guesslabel)

        self.guesspro = QLabel("Possibility: ")
        self.guesspro.setFont(QFont("Consolas", 15))
        self.guesspro.setVisible(False)
        self.vlayout.addWidget(self.guesspro)

        self.vlayout.addStretch()
        self.setLayout(self.vlayout)


class Ttest(QWidget):
    def __init__(self, *args, **kwargs):
        super(Ttest, self).__init__(*args, **kwargs)

        self.vlayout = QVBoxLayout()
        self.vlayout.addStretch()

        self.goBtn = QPushButton("Test!")
        # self.goBtn.setFont(QFont("Consolas", 20))
        self.vlayout.addWidget(self.goBtn)

        self.vlayout.addStretch()
        self.lossLabel = QLabel("Test Loss: ")
        self.lossLabel.setFont(QFont("Consolas", 15))
        self.vlayout.addWidget(self.lossLabel)
        self.accLabel = QLabel("Test Acc: ")
        self.accLabel.setFont(QFont("Consolas", 15))
        self.vlayout.addWidget(self.accLabel)

        self.vlayout.addStretch()
        self.setLayout(self.vlayout)


class TestWidget(QWidget):

    guess = []
    label = []
    class_names = []
    now_file = True

    def __init__(self, *args, **kwargs):
        super(TestWidget, self).__init__(*args, **kwargs)
        self.hlayout = QHBoxLayout()

        self.TIM = TimgWidget()
        self.hlayout.addWidget(self.TIM)

        self.TB = Tbatch()
        self.hlayout.addWidget(self.TB)

        self.TT = Ttest()
        self.hlayout.addWidget(self.TT)

        self.setLayout(self.hlayout)

        with open("./stylesheet/input.qss", "r") as f:
            self.setStyleSheet(f.read())

        self.TIM.ChooseFileBtn.clicked.connect(self.Choose_Btn)
        self.TIM.ChooseImgBtn.clicked.connect(self.img_Btn)
        self.TIM.fileToggle.clicked.connect(self.toggle_file)
        self.TT.goBtn.clicked.connect(self.runTest)
        self.TT.goBtn.setEnabled(False)
        self.TB.imglabel.setFixedSize(250, 250)

        self.warning = QMessageBox()

    def Choose_Btn(self):
        if page_training.uid != None:
            self.TT.goBtn.setEnabled(True)
        else:
            self.TT.goBtn.setEnabled(False)
        print("open folder")
        folder_path = QFileDialog.getOpenFileName(
            self, "Select .npz file", ".", "*.npz")  # start path
        print(folder_path[0])
        self.TIM.filePathEdit.setText(folder_path[0])

        T = np.load(folder_path[0])
        img = T['test_img']
        imgplt = tf.keras.preprocessing.image.array_to_img(img[0])
        imgqt = ImageQt(imgplt)
        self.TB.imglabel.setPixmap(QPixmap.fromImage(imgqt))

        # Store label
        npz = np.load(folder_path[0])
        testY = npz['test_lab']
        self.label.clear()
        for i in testY:
            self.label.append(i)

        # Read class name
        self.class_names.clear()
        with open(folder_path[0] + ".txt", "r") as f:
            for line in f.readlines():
                line = line.strip("\n")
                self.class_names.append(line)
        print(self.class_names)

    def img_Btn(self):
        if page_training.uid != None:
            self.TT.goBtn.setEnabled(True)
        else:
            self.TT.goBtn.setEnabled(False)
        print("open folder")
        folder_path = QFileDialog.getOpenFileName(
            self, "Select img file", "C:/", "Images (*.jpg *.png *.jpeg)")
        print(folder_path[0])
        self.TIM.filePathEdit.setText(folder_path[0])

        self.class_names.clear()
        with open("default/" + str(page_model.default_data) + ".txt", "r") as f:
            for line in f.readlines():
                line = line.strip("\n")
                self.class_names.append(line)
        print(self.class_names)

        self.TB.imglabel.setPixmap(QPixmap(folder_path[0]))

    def toggle_file(self):
        self.now_file ^= 1
        self.TIM.ChooseFileBtn.setVisible(
            self.TIM.ChooseFileBtn.isVisible() ^ 1)
        self.TIM.batchlabel.setVisible(self.TIM.batchlabel.isVisible() ^ 1)
        self.TIM.batchBox.setVisible(self.TIM.batchBox.isVisible() ^ 1)
        self.TT.lossLabel.setVisible(self.TT.lossLabel.isVisible() ^ 1)
        self.TT.accLabel.setVisible(self.TT.accLabel.isVisible() ^ 1)

        self.TT.lossLabel.setText("Test Loss: ")
        self.TT.accLabel.setText("Test Acc: ")

        # self.TB.imgshow.setVisible(self.TB.imgshow.isVisible()^1)
        self.TIM.ChooseImgBtn.setVisible(self.TIM.ChooseImgBtn.isVisible() ^ 1)
        # self.TB.imglabel.setVisible(self.TB.imglabel.isVisible()^1)
        self.TB.guesslabel.setVisible(self.TB.guesslabel.isVisible() ^ 1)
        self.TB.guesspro.setVisible(self.TB.guesspro.isVisible() ^ 1)

        self.TB.guesslabel.setText("Predict: ")
        self.TB.guesspro.setText("Probability: ")

    def runTest(self):
        if self.now_file == True:
            self.thread = Thread(
                page_training.uid, self.TB.batchBox.value(), self.TIM.filePathEdit.text())
            self.thread.response_signal.connect(self.updateLabel)
            self.thread.error_signal.connect(self.error_show)
            self.thread.guess_signal.connect(self.update_guess)
            self.thread.start()
        else:
            dataset = page_model.default_data
            if dataset == 0:
                self.thread = Thread2(page_training.uid, page_input.imgH,
                                      page_input.imgW, page_input.imgC, self.TIM.filePathEdit.text())
            elif dataset == 1 or dataset == 2:
                self.thread = Thread2(
                    page_training.uid, 28, 28, 0, self.TIM.filePathEdit.text())
            else:
                self.thread = Thread2(
                    page_training.uid, 32, 32, 1, self.TIM.filePathEdit.text())
            self.thread.error_signal2.connect(self.error_show)
            self.thread.response_signal2.connect(self.prediction)
            self.thread.start()

    def updateLabel(self, loss, acc):
        self.TT.lossLabel.setText("Test Loss: " + str(loss))
        self.TT.accLabel.setText(f'Test Acc: {(acc * 100):.2f} %')

    def update_guess(self, g):
        self.guess.append(g)

    def prediction(self, guess, pro):
        self.TB.guesslabel.setText("Predict: " + self.class_names[guess])
        self.TB.guesspro.setText(f'Probability: {(pro * 100):.2f} %')

    def error_show(self, msg):
        self.warning.setText(msg)
        self.warning.setIcon(QMessageBox.Icon.Warning)
        self.warning.setWindowTitle("RunTime Error")
        self.warning.show()

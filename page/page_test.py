from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import pathlib, requests, re, socket, page_training, page_input
import numpy as np

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
    def __init__(self):
        super(Thread2, self).__init__()

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
        self.vlayout.addWidget(self.filePathEdit)
             
        self.hlayout = QHBoxLayout()
        self.ChooseFileBtn = QPushButton('NPZ')
        self.ChooseFileBtn.setFixedWidth(150)
        self.ChooseImgBtn = QPushButton('IMG')
        self.ChooseImgBtn.setFixedWidth(150)
        self.ChooseImgBtn.setVisible(False)

        self.hlayout.addWidget(self.ChooseFileBtn)
        self.hlayout.addWidget(self.ChooseImgBtn)
        
        self.vlayout.addLayout(self.hlayout)
        self.vlayout.addStretch()
        self.setLayout(self.vlayout)

class Tbatch(QWidget):
    def __init__(self, *args, **kwargs):
        super(Tbatch, self).__init__(*args, **kwargs)

        self.vlayout = QVBoxLayout()
        self.vlayout.addStretch()
        self.batchlabel = QLabel("batch : ")
        self.batchlabel.setFont(QFont("Consolas", 15))
        self.vlayout.addWidget(self.batchlabel)
        self.batchBox = QSpinBox()
        self.batchBox.setRange(1, 100000)
        self.batchBox.setFixedWidth(150)
        self.vlayout.addWidget(self.batchBox)
        
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



    def toggle_file(self):
        self.now_file ^= 1
        self.TIM.ChooseFileBtn.setVisible(self.TIM.ChooseFileBtn.isVisible()^1)
        self.TB.batchlabel.setVisible(self.TB.batchlabel.isVisible()^1)
        self.TB.batchBox.setVisible(self.TB.batchBox.isVisible()^1)
        self.TIM.ChooseImgBtn.setVisible(self.TIM.ChooseImgBtn.isVisible()^1)
        
    def runTest(self):
        if self.now_file == True:
            self.thread = Thread(page_training.uid, self.TB.batchBox.value(), self.TIM.filePathEdit.text())
            self.thread.response_signal.connect(self.updateLabel)
            self.thread.error_signal.connect(self.error_show)
            self.thread.guess_signal.connect(self.update_guess)
            self.thread.start()

    def updateLabel(self, loss, acc):
        self.TT.lossLabel.setText("Test Loss: " + str(loss))
        self.TT.accLabel.setText("Test Acc: " + str(acc * 100) + " %")
    
    def update_guess(self, g):
        self.guess.append(g)
    
    def error_show(self, msg):
        self.warning.setText(msg)
        self.warning.setIcon(QMessageBox.Icon.Warning)
        self.warning.setWindowTitle("RunTime Error")
        self.warning.show()        
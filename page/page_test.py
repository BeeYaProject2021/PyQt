from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import pathlib, requests, re, socket, page_training

class Thread(QThread):

    response_signal = pyqtSignal(float, float)

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

        ClientSocket = socket.socket()
        ClientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
        loss, acc = data[1], data[2]
        print(loss, acc)
        self.response_signal.emit(float(loss), float(acc))


class TimgWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super(TimgWidget, self).__init__(*args, **kwargs)

        self.vlayout = QVBoxLayout()
        self.vlayout.addStretch()

        # self.ansBox = QComboBox()
        # ansfunctions = ['Have ans', 'NO ans']
        # self.ansBox.addItems(ansfunctions)
        # self.vlayout.addWidget(self.ansBox)

        self.filePathEdit = QLabel()
        self.filePathEdit.setObjectName("Path")
        self.vlayout.addWidget(self.filePathEdit)
        
        self.hlayout = QHBoxLayout()
        self.ChoeseFileBtn = QPushButton('Choese')
        self.ChoeseFileBtn.setFixedWidth(150)
        self.hlayout.addWidget(self.ChoeseFileBtn)
        
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

        self.TIM.ChoeseFileBtn.clicked.connect(self.choese_Btn)
        self.TT.goBtn.clicked.connect(self.runTest)


    def choese_Btn(self):
        if page_training.uid != None:
            self.TT.goBtn.setEnabled(True)
        else:
            self.TT.goBtn.setEnabled(False)
        print("open folder")
        folder_path = QFileDialog.getOpenFileName(
            self, "Select .npz file", ".", "*.npz")  # start path
        print(folder_path[0])
        self.TIM.filePathEdit.setText(folder_path[0])

    def runTest(self):
        self.thread = Thread(page_training.uid, self.TB.batchBox.value(), self.TIM.filePathEdit.text())
        self.thread.response_signal.connect(self.updateLabel)
        self.thread.start()

    def updateLabel(self, loss, acc):
        self.TT.lossLabel.setText("Test Loss: " + str(loss))
        self.TT.accLabel.setText("Test Acc: " + str(acc * 100) + " %")
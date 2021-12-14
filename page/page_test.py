from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import pathlib, requests, re, socket

uid = None

class Thread(QThread):
    def __init__(self, batch):
        super(Thread, self).__init__()
        self.batch = batch

    def run(self):
        global uid
        batch = self.batch

        url = 'http://140.136.204.132:8000/test/'
        x = requests.post(url, data={'uid': uid, 'batch': batch}, 
        files={'file': open(self.datasetPath, 'rb')})    
        print(x.text)
        data = re.split(" |\"", x.text)
        print("response data", data)

        ClientSocket = socket.socket()
        ClientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        host = '140.136.204.132'
        # port = (int)(data[3])



class TimgWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super(TimgWidget, self).__init__(*args, **kwargs)

        self.vlayout = QVBoxLayout()
        self.vlayout.addStretch()

        # self.ansBox = QComboBox()
        # ansfunctions = ['Have ans', 'NO ans']
        # self.ansBox.addItems(ansfunctions)
        # self.vlayout.addWidget(self.ansBox)


        self.hlayout = QHBoxLayout()

        self.filePathEdit = QLineEdit()
        self.filePathEdit.setFixedWidth(200)
        self.hlayout.addWidget(self.filePathEdit)

        self.ChoeseFileBtn = QPushButton('Choese')
        self.hlayout.addWidget(self.ChoeseFileBtn)
        self.hlayout.addStretch()
        self.vlayout.addLayout(self.hlayout)
        self.vlayout.addStretch()
        self.setLayout(self.vlayout)

class Tbatch(QWidget):
    def __init__(self, *args, **kwargs):
        super(Tbatch, self).__init__(*args, **kwargs)

        self.vlayout = QVBoxLayout()
        self.vlayout.addStretch()
        self.batchlabel = QLabel("batch : ")
        self.vlayout.addWidget(self.batchlabel)
        self.batchBox = QSpinBox()
        self.batchBox.setRange(1, 100000)
        self.vlayout.addWidget(self.batchBox)

        self.vlayout.addStretch()
        self.setLayout(self.vlayout)


class TestWidget(QWidget):

    def __init__(self, *args, **kwargs):
        super(TestWidget, self).__init__(*args, **kwargs)
        self.hlayout = QHBoxLayout()
        
        self.TIM = TimgWidget()
        self.hlayout.addWidget(self.TIM)
        self.hlayout.addStretch()

        self.TB = Tbatch()
        self.hlayout.addWidget(self.TB)
        self.hlayout.addStretch()
        self.setLayout(self.hlayout)

        self.TIM.ChoeseFileBtn.clicked.connect(self.choese_Btn)

        self.goBtn = QPushButton("Test!", self)
        self.goBtn.clicked.connect(self.runTest)
        self.hlayout.addWidget(self.goBtn)

    def choese_Btn(self):
        print("open folder")
        folder_path = QFileDialog.getExistingDirectory(
            self, "Open folder", "./")  # start path

        # if folder_path:
        #     self.start_loading(folder_path)

        self.TIM.filePathEdit.setText(folder_path)
        folder_path = pathlib.Path(folder_path)

    def runTest(self):
        self.thread = Thread(self.TB.batchBox.value)

        self.thread.start()
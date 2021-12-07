from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import pathlib

class TimgWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super(TimgWidget, self).__init__(*args, **kwargs)

        self.hlayout = QHBoxLayout()

        self.filePathEdit = QLineEdit()
        self.filePathEdit.setFixedWidth(200)
        self.hlayout.addWidget(self.filePathEdit)

        self.ChoeseFileBtn = QPushButton('Choese')
        self.hlayout.addWidget(self.ChoeseFileBtn)

class Tbatch(QWidget):
    def __init__(self, *args, **kwargs):
        super(TimgWidget, self).__init__(*args, **kwargs)

        self.vlayout = QVBoxLayout()
        self.vlayout.addStretch()

        self.batchBox = QSpinBox()
        self.batchBox.setRange(1, 100000)
        self.vlayout.addWidget(self.batchBox)

        self.vlayout.addStretch()


class TestWidget(QWidget):

    def __init__(self, *args, **kwargs):
        super(TestWidget, self).__init__(*args, **kwargs)
        self.hlayout = QHBoxLayout()
        
        self.TIM = TimgWidget()
        self.hlayout.addWidget(self.TIM)

        self.TB = Tbatch()
        self.hlayout.addWidget(self.TB)

        self.TIM.ChoeseFileBtn.clicked.connect(self.choese_Btn)

    def choese_Btn(self):
        self.PlaySound()
        print("open folder")
        folder_path = QFileDialog.getExistingDirectory(
            self, "Open folder", "./")  # start path

        if folder_path:
            self.start_loading(folder_path)

        self.imgw.filePathEdit.setText(folder_path)
        folder_path = pathlib.Path(folder_path)
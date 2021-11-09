import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Information(QWidget):
    def __init__(self):
        super(Information, self).__init__()

        self.vinformation = QVBoxLayout()
        self.notes = QLabel()
        self.notes.setText("將左方的layer拖拉至中央範圍內\n會看到兩綠點\n可用右鍵將兩layer連接\n欲刪除可使用左鍵框起來不要的使用delete鍵刪除")
        self.vinformation.addWidget(self.notes)
        self.setLayout(self.vinformation)
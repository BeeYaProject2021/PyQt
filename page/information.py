from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QApplication


class Information(QWidget):
    def __init__(self):
        super(Information, self).__init__()
        self.setStyleSheet('background-color: white;')
        # self.setStyleSheet('background-color: white;',"QLabel(color:rgb(0,100,100,250));")
        # string value
        title = "Information"
        # set the title
        self.setWindowTitle(title)
        self.vinformation = QVBoxLayout()
        self.notes = QLabel()
        self.notes.setText(
            "將左方的layer拖拉至中間畫布內，可用右鍵將兩layer以綠點連接\n欲刪除時，可使用左鍵框起來要刪除的元素，按下delete鍵刪除")
        self.notes.setFont(QFont("Roman times", 20, QFont.Bold))
        # self.notes.styleSheet("color : red")
        self.vinformation.addWidget(self.notes)
        self.setLayout(self.vinformation)

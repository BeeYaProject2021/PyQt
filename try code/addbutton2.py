import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("my window")
        self.num = 2

        #creating a button to be clicked
        button1 = QPushButton('Button-1', self)
#        button1.move(100, 70)
        button1.clicked.connect(self.on_click)     

        self.layout = QVBoxLayout(self) 
        self.layout.addWidget(button1)        

    @pyqtSlot()
    def on_click(self):
        print('Button-{} will be created'.format(self.num))
        button2 = QPushButton('Button-{}'.format(self.num), self)
        button2.clicked.connect(lambda : print(button2.text()))
#        button2.move(100, 200)

        self.layout.addWidget(button2)
        self.num += 1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
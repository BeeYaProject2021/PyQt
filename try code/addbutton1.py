import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("my window")
        self.setGeometry(100, 100, 320, 300)

        #creating a button to be clicked
        button1 = QPushButton('Button-1', self)
        button1.move(100, 70)
        button1.clicked.connect(self.on_click)      # button1

    @pyqtSlot()
    def on_click(self):
        print('Button-2 will be created')
        button2 = QPushButton('Button-2', self)
        button2.move(100, 200)
        button2.show()                              # +++

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())


# import sys
# from PyQt5 import QtCore, QtWidgets

# class TabPage(QtWidgets.QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         group = QtWidgets.QGroupBox('Monty Python')
#         layout = QtWidgets.QVBoxLayout(self)
#         layout.addWidget(group)
#         grid = QtWidgets.QGridLayout(group)
#         grid.addWidget(QtWidgets.QLabel('Enter a name:'), 0, 0)
#         grid.addWidget(QtWidgets.QLabel('Choose a number:'), 0, 1)
#         grid.addWidget(QtWidgets.QLineEdit(), 1, 0)
#         grid.addWidget(QtWidgets.QComboBox(), 1, 1)
#         grid.addWidget(QtWidgets.QPushButton('Click Me!'), 1, 2)
#         grid.addWidget(QtWidgets.QSpinBox(), 2, 0)
#         grid.addWidget(QtWidgets.QPushButton('Clear Text'), 2, 2)
#         grid.addWidget(QtWidgets.QTextEdit(), 3, 0, 1, 3)

# class Window(QtWidgets.QWidget):
#     def __init__(self):
#         super().__init__()
#         self.tabs = QtWidgets.QTabWidget()
#         layout = QtWidgets.QVBoxLayout(self)
#         layout.addWidget(self.tabs)
#         button = QtWidgets.QToolButton()
#         button.setToolTip('Add New button')
#         button.clicked.connect(self.addNewbutton)
#         button.setIcon(self.style().standardIcon(
#             QtWidgets.QStyle.SP_DialogYesButton))
#         self.tabs.setCornerWidget(button, QtCore.Qt.TopRightCorner)
#         self.addNewbutton()

#     def addNewbutton(self):
#         text = 'Add New button'
#         self.tabs.addbutton(TabPage(self.bu), text)

# if __name__ == '__main__':

#     app = QtWidgets.QApplication(sys.argv)
#     window = Window()
#     window.setGeometry(600, 100, 300, 200)
#     window.show()
#     sys.exit(app.exec_())
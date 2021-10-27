# importing libraries
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
 
 
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
 
        # setting title
        self.setWindowTitle("Python ")
 
        # setting geometry
        self.setGeometry(100, 100, 600, 400)
 
        # creating a button
        self.button = QPushButton("CLICK", self)
 
        # setting up the geometry
        self.button.setGeometry(200, 150, 200, 40)
 
        # connecting method when button get clicked
        self.button.clicked.connect(self.clickme)
 
        # showing all the widgets
        self.show()
 
    # action method
    def clickme(self):
 
        # hiding the button
        self.button.deleteLater()
        # printing pressed
        print("pressed")
 
# create pyqt5 app
App = QApplication(sys.argv)
 
# create the instance of our Window
window = Window()
 
# start the app
sys.exit(App.exec())
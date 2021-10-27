import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget
 
class Logo(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
 
    def initUI(self):
        # self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('MyLogo')
        # self.move(300, 300)
        self.setWindowIcon(QIcon('Logo.ico'))
        self.show()
 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Logo()
    sys.exit(app.exec_())
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class Combo(QComboBox):
    def __init__(self,title,parent):
        super(Combo, self).__init__(parent)
        #設置爲可接受拖曳操作文本
        self.setAcceptDrops(True)

    #當執行一個拖曳控件操作，並且鼠標指針進入該控件時，這個事件將會被觸發。
    # 在這個事件中可以獲得被操作的窗口控件，還可以有條件地接受或拒絕該拖曳操作
    def dragEnterEvent(self,e):
        #檢測拖曳進來的數據是否包含文本，如有則接受，無則忽略
        if e.mimeData().hasText():
            e.accept()
        else:
            e.ignore()
    #當拖曳操作在其目標控件上被釋放時，這個事件將被觸發
    def dropEvent(self,e):
        #添加拖曳文本到條目中
        self.addItem(e.mimeData().text())
class Example(QWidget):
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()

    def initUI(self):
        #表單佈局，添加控件
        lo=QFormLayout()
        lo.addRow(QLabel('請把左邊的文本拖曳到右邊的下拉菜單中'))

        #實例化單行文本框，設置爲允許拖曳操作
        edit=QLineEdit()
        edit.setDragEnabled(True)

        #實例化Combo對象，添加控件到佈局中
        com=Combo('Button',self)
        lo.addRow(edit,com)

        #設置主窗口布局及標題
        self.setLayout(lo)
        self.setWindowTitle('簡單的拖曳例子')

if __name__ == '__main__':
    app=QApplication(sys.argv)
    ex=Example()
    ex.show()
    sys.exit(app.exec_())
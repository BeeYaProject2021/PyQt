# import imp
# import os
# import sys
# import pathlib
# import PIL
# import PIL.Image
# import numpy as np
# import tensorflow as tf
# from PyQt5 import QtWidgets
# from PyQt5.QtCore import *
# from PyQt5.QtWidgets import *
# from PyQt5.QtGui import *

# class TabBar(QTabBar):
#     def tabSizeHint(self, index):
#         size = QTabBar.tabSizeHint(self, index)
#         w = int(self.width()/self.count())
#         print(self.width())
#         return QSize(w, size.height())

# class MainWindow(QMainWindow):
#     def __init__(self, *args, **kwargs):
#         super(MainWindow, self).__init__(*args, **kwargs)

# data_dir = pathlib.Path("C:/Users/user/Desktop/PyQt/try code/image")
# allFileList = os.listdir(data_dir)
# for i in allFileList:
#     filelist = pathlib.Path(str(data_dir) + '/' + i)
#     allList = os.walk(filelist)
#     print(allList)
# allList = os.walk(data_dir)
# for dirs, files in allList:
#     print("directory：", dirs)
#     print("file：", files)



# app = QApplication(sys.argv)
# window = MainWindow()
# app.exec_()

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTreeView, QFileSystemModel, QVBoxLayout
from PyQt5.QtCore import QModelIndex

class FileSystemView(QWidget):
	def __init__(self, dir_path):
		super().__init__()
		appWidth = 800
		appHeight = 300
		self.setWindowTitle('File System Viewer')
		self.setGeometry(300, 300, appWidth, appHeight)
		
		self.model = QFileSystemModel()
		self.model.setRootPath(dir_path)
		self.tree =  QTreeView()
		self.tree.setModel(self.model)
		self.tree.setRootIndex(self.model.index(dirPath))
		self.tree.setColumnWidth(0, 250)
		self.tree.setAlternatingRowColors(True)

		layout = QVBoxLayout()
		layout.addWidget(self.tree)
		self.setLayout(layout)

if __name__ == '__main__':
	app = QApplication(sys.argv)
	dirPath = r'C:/Users/user/Desktop/PyQt/try code/image'
	demo = FileSystemView(dirPath)
	demo.show()
	sys.exit(app.exec_())
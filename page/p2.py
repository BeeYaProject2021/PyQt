# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'p2.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow2(object):
    def setupUi(self, MainWindow2):
        MainWindow2.setObjectName("MainWindow2")
        MainWindow2.resize(960, 868)
        self.centralwidget = QtWidgets.QWidget(MainWindow2)
        self.centralwidget.setObjectName("centralwidget")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(0, 0, 151, 751))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 149, 749))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.conv2D = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.conv2D.setGeometry(QtCore.QRect(30, 80, 81, 31))
        self.conv2D.setObjectName("conv2D")
        self.maxpooling2D = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.maxpooling2D.setGeometry(QtCore.QRect(30, 150, 81, 31))
        self.maxpooling2D.setObjectName("maxpooling2D")
        self.flatten = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.flatten.setGeometry(QtCore.QRect(30, 220, 81, 31))
        self.flatten.setObjectName("flatten")
        self.dense = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.dense.setGeometry(QtCore.QRect(30, 290, 81, 31))
        self.dense.setObjectName("dense")
        self.garbage_can = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.garbage_can.setGeometry(QtCore.QRect(40, 600, 61, 81))
        self.garbage_can.setText("")
        self.garbage_can.setObjectName("garbage_can")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.previous = QtWidgets.QPushButton(self.centralwidget)
        self.previous.setGeometry(QtCore.QRect(760, 0, 35, 35))
        self.previous.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("rotate-left 4.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.previous.setIcon(icon)
        self.previous.setObjectName("previous")
        self.nextstep = QtWidgets.QPushButton(self.centralwidget)
        self.nextstep.setGeometry(QtCore.QRect(800, 0, 35, 35))
        self.nextstep.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("rotate-right 2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.nextstep.setIcon(icon1)
        self.nextstep.setObjectName("nextstep")
        self.stop = QtWidgets.QPushButton(self.centralwidget)
        self.stop.setGeometry(QtCore.QRect(920, 0, 35, 35))
        self.stop.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("4_audio_pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.stop.setIcon(icon2)
        self.stop.setObjectName("stop")
        self.suspend = QtWidgets.QPushButton(self.centralwidget)
        self.suspend.setGeometry(QtCore.QRect(880, 0, 35, 35))
        self.suspend.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("4_audio_stop.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.suspend.setIcon(icon3)
        self.suspend.setObjectName("suspend")
        self.start = QtWidgets.QPushButton(self.centralwidget)
        self.start.setGeometry(QtCore.QRect(840, 0, 35, 35))
        self.start.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("4_audio_play.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.start.setIcon(icon4)
        self.start.setObjectName("start")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(170, 40, 781, 711))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea_2 = QtWidgets.QScrollArea(self.verticalLayoutWidget)
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setEnabled(True)
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 777, 707))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.verticalLayout.addWidget(self.scrollArea_2)
        self.show_file_path = QtWidgets.QTextBrowser(self.centralwidget)
        self.show_file_path.setGeometry(QtCore.QRect(10, 760, 401, 51))
        self.show_file_path.setObjectName("show_file_path")
        self.show_folder_path = QtWidgets.QTextBrowser(self.centralwidget)
        self.show_folder_path.setGeometry(QtCore.QRect(430, 760, 401, 51))
        self.show_folder_path.setObjectName("show_folder_path")
        MainWindow2.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow2)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 960, 26))
        self.menubar.setObjectName("menubar")
        self.menufile = QtWidgets.QMenu(self.menubar)
        self.menufile.setObjectName("menufile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        self.menuRun = QtWidgets.QMenu(self.menubar)
        self.menuRun.setObjectName("menuRun")
        self.menuTool = QtWidgets.QMenu(self.menubar)
        self.menuTool.setObjectName("menuTool")
        self.menuSetting = QtWidgets.QMenu(self.menubar)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("gear.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.menuSetting.setIcon(icon5)
        self.menuSetting.setObjectName("menuSetting")
        MainWindow2.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow2)
        self.statusbar.setObjectName("statusbar")
        MainWindow2.setStatusBar(self.statusbar)
        self.actionNew = QtWidgets.QAction(MainWindow2)
        self.actionNew.setObjectName("actionNew")
        self.actionSave = QtWidgets.QAction(MainWindow2)
        self.actionSave.setObjectName("actionSave")
        self.actionSave_as = QtWidgets.QAction(MainWindow2)
        self.actionSave_as.setObjectName("actionSave_as")
        self.actionSave_all = QtWidgets.QAction(MainWindow2)
        self.actionSave_all.setObjectName("actionSave_all")
        self.actionClose = QtWidgets.QAction(MainWindow2)
        self.actionClose.setObjectName("actionClose")
        self.actionQuit = QtWidgets.QAction(MainWindow2)
        self.actionQuit.setObjectName("actionQuit")
        self.actionCut = QtWidgets.QAction(MainWindow2)
        self.actionCut.setObjectName("actionCut")
        self.actionCopy = QtWidgets.QAction(MainWindow2)
        self.actionCopy.setObjectName("actionCopy")
        self.actionPaste = QtWidgets.QAction(MainWindow2)
        self.actionPaste.setObjectName("actionPaste")
        self.actionDelete = QtWidgets.QAction(MainWindow2)
        self.actionDelete.setObjectName("actionDelete")
        self.actionSelete_All = QtWidgets.QAction(MainWindow2)
        self.actionSelete_All.setObjectName("actionSelete_All")
        self.actionOpen_file = QtWidgets.QAction(MainWindow2)
        self.actionOpen_file.setObjectName("actionOpen_file")
        self.actionOpen_folder = QtWidgets.QAction(MainWindow2)
        self.actionOpen_folder.setObjectName("actionOpen_folder")
        self.menufile.addAction(self.actionNew)
        self.menufile.addAction(self.actionOpen_file)
        self.menufile.addAction(self.actionOpen_folder)
        self.menufile.addSeparator()
        self.menufile.addAction(self.actionSave)
        self.menufile.addAction(self.actionSave_as)
        self.menufile.addAction(self.actionSave_all)
        self.menufile.addSeparator()
        self.menufile.addAction(self.actionClose)
        self.menufile.addAction(self.actionQuit)
        self.menuEdit.addAction(self.actionCut)
        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addAction(self.actionPaste)
        self.menuEdit.addAction(self.actionDelete)
        self.menuEdit.addAction(self.actionSelete_All)
        self.menubar.addAction(self.menufile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuRun.menuAction())
        self.menubar.addAction(self.menuTool.menuAction())
        self.menubar.addAction(self.menuSetting.menuAction())

        self.retranslateUi(MainWindow2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow2)

    def retranslateUi(self, MainWindow2):
        _translate = QtCore.QCoreApplication.translate
        MainWindow2.setWindowTitle(_translate("MainWindow2", "MainWindow"))
        self.conv2D.setText(_translate("MainWindow2", "conv2D"))
        self.maxpooling2D.setText(_translate("MainWindow2", "maxpooling2D"))
        self.flatten.setText(_translate("MainWindow2", "flatten"))
        self.dense.setText(_translate("MainWindow2", "dense"))
        self.menufile.setTitle(_translate("MainWindow2", "File"))
        self.menuEdit.setTitle(_translate("MainWindow2", "Edit"))
        self.menuView.setTitle(_translate("MainWindow2", "View"))
        self.menuRun.setTitle(_translate("MainWindow2", "Run"))
        self.menuTool.setTitle(_translate("MainWindow2", "Tool"))
        self.menuSetting.setTitle(_translate("MainWindow2", "Setting"))
        self.actionNew.setText(_translate("MainWindow2", "New"))
        self.actionSave.setText(_translate("MainWindow2", "Save"))
        self.actionSave_as.setText(_translate("MainWindow2", "Save as"))
        self.actionSave_all.setText(_translate("MainWindow2", "Save all"))
        self.actionClose.setText(_translate("MainWindow2", "Close"))
        self.actionQuit.setText(_translate("MainWindow2", "Quit"))
        self.actionCut.setText(_translate("MainWindow2", "Cut"))
        self.actionCopy.setText(_translate("MainWindow2", "Copy"))
        self.actionPaste.setText(_translate("MainWindow2", "Paste"))
        self.actionDelete.setText(_translate("MainWindow2", "Delete"))
        self.actionSelete_All.setText(_translate("MainWindow2", "Select All"))
        self.actionOpen_file.setText(_translate("MainWindow2", "Open file"))
        self.actionOpen_folder.setText(_translate("MainWindow2", "Open folder"))

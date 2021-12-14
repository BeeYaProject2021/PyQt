from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from page_setting import *
from page_model import *
from page_input import *
from page_training import *
from page_test import *
from screenshot import *
from information import *

import os
import sys


class TabBar(QTabBar):
    def tabSizeHint(self, index):
        size = QTabBar.tabSizeHint(self, index)
        w = int(self.width()/self.count())
        print(self.width())
        return QSize(w, size.height())


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.tabs = QTabWidget()
        self.tb = TabBar()
        # label = "Blank"
        # a = WidgetA(self)
        # i = self.tb.addTab(label)
        # self.tb.setCurrentIndex(i)
        # self.tabs.setTabBar(self.tb)

        # self.tabs.setStyleSheet(
        #     "QTabBar::tab::first { height: 100px; width: 100px; background: 'red'}")
        label = "Dataset"
        self.inputW = InputWidget()
        i = self.tabs.addTab(self.inputW, label)
        self.inputW.img_total_signal.connect(self.img_signal_acc)
        self.inputW.img_size_signal.connect(self.img_size_signal_acc)

        label = "Model"
        self.modelW = ModelWidget()
        i = self.tabs.addTab(self.modelW, label)
        self.modelW.layer_json_signal.connect(self.layer_json_signal_acc)

        label = "Training Setting"
        self.settingW = SettingWidget()
        self.settingW.batch_epoch_signal.connect(self.batch_epoch_signal_acc)
        i = self.tabs.addTab(self.settingW, label)

        label = "Result"
        self.trainingW = TrainingWidget()
        i = self.tabs.addTab(self.trainingW, label)

        label = "Test"
        self.testW = TestWidget()
        i = self.tabs.addTab(self.testW, label)
        self.tabs.setCurrentIndex(0)
        # self.tabs.setDocumentMode(True)
        # self.tabs.currentChanged.connect(self.current_tab_changed)
        with open("./stylesheet/main.qss", "r") as f:
            self.setStyleSheet(f.read())
        self.setCentralWidget(self.tabs)
        self.resize(1280, 720)
        self.show()

        self.cutscerrn = CaptureScreen()
        self.trainingW.toolButton_4.clicked.connect(self.cutscerrn.show)

        self.modelinformation = Information()
        self.modelW.layerm.binformation.clicked.connect(
            self.modelinformation.show)

    def img_signal_acc(self, msg):
        self.trainingW.img_total = msg

    def img_size_signal_acc(self, h, w, color):
        self.modelW.input_shape[0] = h
        self.modelW.input_shape[1] = w
        self.modelW.input_shape[2] = color

    def batch_epoch_signal_acc(self, batch, epoch, setting_json):
        self.trainingW.batch_size = batch
        self.trainingW.epoch = epoch
        self.trainingW.setting_json = setting_json

    def layer_json_signal_acc(self, json_str, dataset, datasetPath):
        self.trainingW.layer_json = json_str
        self.trainingW.dataset = dataset
        self.trainingW.datasetPath = datasetPath

        # keyboard.wait(hotkey='c')
app = QApplication(sys.argv)

window = MainWindow()

app.exec_()

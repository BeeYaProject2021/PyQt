import os
import pathlib
import PIL
import PIL.Image
import numpy as np
import tensorflow as tf
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import time
from PyQt5.QtCore import QThread, pyqtSignal


class SettingWidget(QWidget):
    batch_epoch_signal = pyqtSignal(int, int, str)

    def __init__(self, *args, **kwargs):
        super(SettingWidget, self).__init__(*args, **kwargs)

        self.vlayout = QVBoxLayout()
        self.vlayout.addStretch()

        self.optLabel = QLabel()
        self.optLabel.setText("Optimizer")
        self.vlayout.addWidget(self.optLabel)

        self.optBox = QComboBox()
        optimizers = ['SGD', 'RMSprop', 'Adam', 'Adadelta',
                      'Adagrad', 'Adamax', 'Nadam', 'Ftrl']
        self.optBox.addItems(optimizers)
        self.optBox.currentIndexChanged.connect(self.display)
        self.vlayout.addWidget(self.optBox)

        self.lrLabel = QLabel()
        self.lrLabel.setText("Learning Rate (0 < LR < 1)")
        self.vlayout.addWidget(self.lrLabel)

        self.learning_rateBox = QDoubleSpinBox()
        self.learning_rateBox.setDecimals(4)
        self.learning_rateBox.setMinimum(0.001)
        self.learning_rateBox.setMaximum(0.999)
        self.learning_rateBox.setSingleStep(0.001)
        self.vlayout.addWidget(self.learning_rateBox)

        self.lossLabel = QLabel()
        self.lossLabel.setText("Loss Function")
        self.vlayout.addWidget(self.lossLabel)

        self.lossBox = QComboBox()
        lossfunctions = ['mean_squared_error', 'mean_absolute_error', 'mean_absolute_percentage_error',
                         'mean_squared_logarithmic_error', 'squared_hinge', 'hinge', 'categorical_hinge', 'logcosh', 'categorical_crossentropy',
                         'sparse_categorical_crossentropy', 'kullback_leibler_divergence', 'poisson',
                         'cosine_proximity']
        self.lossBox.addItems(lossfunctions)
        self.vlayout.addWidget(self.lossBox)

        self.bsLabel = QLabel()
        self.bsLabel.setText("Batch Size")
        self.vlayout.addWidget(self.bsLabel)

        self.batchBox = QSpinBox()
        self.batchBox.setRange(1, 100000)
        self.vlayout.addWidget(self.batchBox)

        self.epochLabel = QLabel()
        self.epochLabel.setText("Epochs")
        self.vlayout.addWidget(self.epochLabel)

        self.epochBox = QSpinBox()
        self.epochBox.setRange(1, 100000)
        self.vlayout.addWidget(self.epochBox)

        self.checkbutton = QPushButton('Click Here To Complete', self)
        self.checkbutton.clicked.connect(self.combine)
        self.vlayout.addWidget(self.checkbutton)

        self.combinedata = QLabel()
        self.combinedata.setText("Data:")

        with open("./stylesheet/setting.qss", "r") as f:
            self.setStyleSheet(f.read())

        self.vlayout.addWidget(self.combinedata)

        self.setLayout(self.vlayout)

    def display(self):
        print(self.optBox.currentIndex())

    def combine(self):
        opt = self.optBox.currentText()
        lr = str(self.learning_rateBox.value())
        loss = self.lossBox.currentText()
        batch = str(self.batchBox.value())
        epoch = str(self.epochBox.value())
        data = "{\"id\":-1,\"optimizer\":\""+opt+"\",\"learning_rate\":\""+lr + \
            "\",\"loss_fn\":\""+loss+"\",\"batch_size\":\"" + \
            batch+"\",\"epochs\":\""+epoch+"\"}]"
        print(opt)
        print(lr)
        print(loss)
        print(batch)
        print(epoch)
        self.batch_epoch_signal.emit(
            self.batchBox.value(), self.epochBox.value(), data)
        self.combinedata.setText("Data:"+data)

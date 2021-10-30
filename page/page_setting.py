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
    def __init__(self, *args, **kwargs):
        super(SettingWidget, self).__init__(*args, **kwargs)

        self.vlayout = QVBoxLayout()
        self.vlayout.addStretch()

        self.optBox = QComboBox()
        optimizers = ['SGD', 'RMSprop', 'Adam', 'Adadelta', 'Adagrad', 'Adamax', 'Nadam', 'Ftrl']
        self.optBox.addItems(optimizers)
        self.optBox.currentIndexChanged.connect(self.display)
        self.vlayout.addWidget(self.optBox)

        self.learning_rateBox = QDoubleSpinBox()
        self.learning_rateBox.setDecimals(4)
        self.learning_rateBox.setMinimum(0.001)
        self.learning_rateBox.setMaximum(0.999)
        self.learning_rateBox.setSingleStep(0.001)
        self.vlayout.addWidget(self.learning_rateBox)

        self.lossBox = QComboBox()
        lossfunctions = ['Binary Cross-entropy', 'Categorical Cross-entropy', 'Categorical Hinge',
         'Cosine Similarity', 'Hinge', 'Huber', 'KL Divergence', 'LogCosh', 'Mean Absolute Error',
         'Mean Absolute Percentage Error', 'Mean Squared Error', 'Mean Squared Logarithmic Error',
         'Poisson', 'Sparse Categorical Cross-entropy', 'Squared Hinge']
        self.lossBox.addItems(lossfunctions)
        self.vlayout.addWidget(self.lossBox)

        self.batchBox = QSpinBox()
        self.batchBox.setMinimum(1)
        self.vlayout.addWidget(self.batchBox)

        self.epochBox = QSpinBox()
        self.epochBox.setMinimum(1)
        self.vlayout.addWidget(self.epochBox)

        self.checkbutton = QPushButton('你要確定捏', self)
        self.vlayout.addWidget(self.checkbutton)

        self.setLayout(self.vlayout)
    
    def display(self):
        print(self.optBox.currentIndex())
import pathlib, PIL, PIL.Image
import numpy as np
import tensorflow as tf
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class AttributeWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super(AttributeWidget, self).__init__(*args, **kwargs)
        self.vlayout = QVBoxLayout()
        self.vlayout.addStretch()

        self.validsplitLabel = QLabel("percentage for validation: ")
        self.validsplitLabel.setFont(QFont("Arial", 15))
        self.vlayout.addWidget(self.validsplitLabel)

        self.validsplitBox = QDoubleSpinBox()
        self.validsplitBox.setRange(0.0, 1.0)
        self.validsplitBox.setSingleStep(0.01)
        self.vlayout.addWidget(self.validsplitBox)

        self.imgsizeLabel = QLabel("image size: ")
        self.imgsizeLabel.setFont(QFont("Arial", 15))
        self.vlayout.addWidget(self.imgsizeLabel)

        self.imgboxLayout = QHBoxLayout()

        self.imghvLayout = QVBoxLayout()
        self.imghLabel = QLabel("height: ")
        self.imghLabel.setFont(QFont("Arial", 10))
        self.imghvLayout.addWidget(self.imghLabel)

        self.imghBox = QSpinBox()
        self.imghBox.setRange(0, 1000)
        self.imghBox.setSingleStep(10)
        self.imghvLayout.addWidget(self.imghBox)

        self.imgboxLayout.addLayout(self.imghvLayout)

        self.imgwvLayout = QVBoxLayout()
        self.imgwLabel = QLabel("width: ")
        self.imgwLabel.setFont(QFont("Arial", 10))
        self.imgwvLayout.addWidget(self.imgwLabel)

        self.imgwBox = QSpinBox()
        self.imgwBox.setRange(0, 1000)
        self.imgwBox.setSingleStep(10)
        self.imgwvLayout.addWidget(self.imgwBox)

        self.imgboxLayout.addLayout(self.imgwvLayout)

        self.vlayout.addLayout(self.imgboxLayout)

        self.confirmBtn = QPushButton('Confirm')
        self.vlayout.addWidget(self.confirmBtn)
        self.confirmBtn.clicked.connect(self.confirm_Btn)

        self.vlayout.addStretch()
        self.setLayout(self.vlayout)

    def confirm_Btn(self, path):
        # Use self and point to get objects in vlayout
        validate = self.b.validsplitBox.value()
        imgH = self.b.imghBox.value()
        imgW = self.b.imgwBox.value()
        print(validate)
        print(imgH, imgW)

        train_ds = tf.keras.preprocessing.image_dataset_from_directory(
            path,
            validation_split=validate,
            subset="training",
            seed=123,
            image_size=(imgH, imgW),
            batch_size=32)

        print(type(train_ds))

class InputWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super(InputWidget, self).__init__(*args, **kwargs)

        self.hlayout = QHBoxLayout()
        self.hlayout.addStretch()
        self.SelectFileBtn = QPushButton('button')
        self.hlayout.addWidget(self.SelectFileBtn)

        self.SelectFileBtn.clicked.connect(self.input_Btn)

        self.hlayout.addStretch()
        self.b = AttributeWidget()
        self.hlayout.addWidget(self.b)
        self.setLayout(self.hlayout)

    def input_Btn(self):
        print("open folder")
        folder_path = QFileDialog.getExistingDirectory(self,
                  "Open folder",
                  "./")                 # start path
        print(folder_path)
        folder_path = pathlib.Path(folder_path)
        print(folder_path)
        img_cnt = len(list(folder_path.glob('*/*.jpg')))
        print(img_cnt)
        roses = list(folder_path.glob('roses/*'))
        x = PIL.Image.open(str(roses[0]))
        x.show()
        

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

class AttributeWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super(AttributeWidget, self).__init__(*args, **kwargs)

        self.vlayout = QVBoxLayout()
        self.vlayout.addStretch()

        self.validsplitLabel = QLabel("percentage for validation: ")
        self.validsplitLabel.setFont(QFont("Arial", 15))
        self.vlayout.addWidget(self.validsplitLabel)

        self.validsplitBox = QDoubleSpinBox()
        self.validsplitBox.setRange(0.01, 1.0)
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
        self.imghBox.setRange(10, 1000)
        self.imghBox.setSingleStep(10)
        self.imghvLayout.addWidget(self.imghBox)

        self.imgboxLayout.addLayout(self.imghvLayout)

        self.imgwvLayout = QVBoxLayout()
        self.imgwLabel = QLabel("width: ")
        self.imgwLabel.setFont(QFont("Arial", 10))
        self.imgwvLayout.addWidget(self.imgwLabel)

        self.imgwBox = QSpinBox()
        self.imgwBox.setRange(10, 1000)
        self.imgwBox.setSingleStep(10)
        self.imgwvLayout.addWidget(self.imgwBox)

        self.imgboxLayout.addLayout(self.imgwvLayout)

        self.vlayout.addLayout(self.imgboxLayout)

        self.confirmBtn = QPushButton('Confirm')
        self.vlayout.addWidget(self.confirmBtn)

        self.progressBar = QProgressBar()
        self.vlayout.addWidget(self.progressBar)
        self.progressBar.setValue(0)
        self.progressBar.setVisible(False)

        self.vlayout.addStretch()
        self.setLayout(self.vlayout)


class ImgWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super(ImgWidget, self).__init__(*args, **kwargs)

        self.hlayout = QHBoxLayout()

        self.filePathEdit = QLineEdit()
        self.filePathEdit.setFixedWidth(200)
        self.hlayout.addWidget(self.filePathEdit)

        self.selectFileBtn = QPushButton('Select')
        self.hlayout.addWidget(self.selectFileBtn)

        self.vlayout = QVBoxLayout()
        self.vlayout.addStretch()

        self.imgLabel = QLabel('Select a folder path for input dataset')
        self.imgLabel.setFont(QFont("Arial", 15))
        self.vlayout.addWidget(self.imgLabel)

        self.vlayout.addLayout(self.hlayout)

        self.vlayout.addStretch()
        self.setLayout(self.vlayout)


class InputWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super(InputWidget, self).__init__(*args, **kwargs)

        self.hlayout = QHBoxLayout()
        self.hlayout.addStretch(1)

        self.imgw = ImgWidget()
        self.hlayout.addWidget(self.imgw)

        self.hlayout.addStretch(1)
        self.aw = AttributeWidget()
        self.hlayout.addWidget(self.aw)

        self.setLayout(self.hlayout)
        self.imgw.selectFileBtn.clicked.connect(self.input_Btn)
        self.aw.confirmBtn.clicked.connect(self.confirm_Btn)

        self.warning = QMessageBox()

    def input_Btn(self):
        print("open folder")
        folder_path = QFileDialog.getExistingDirectory(
            self, "Open folder", "./")  # start path

        self.imgw.filePathEdit.setText(folder_path)
        folder_path = pathlib.Path(folder_path)
        print(folder_path)

        img_cnt = len(list(folder_path.glob('*/*.*')))
        print(img_cnt)
        # roses = list(folder_path.glob('roses/*'))
        # x = PIL.Image.open(str(roses[0]))
        # x.show()

    def confirm_Btn(self):
        # Check Path exists
        if os.path.exists(self.imgw.filePathEdit.text()):

            path = pathlib.Path(self.imgw.filePathEdit.text())
            print(path)

            self.aw.progressBar.setVisible(True)

            validate = self.aw.validsplitBox.value()
            imgH = self.aw.imghBox.value()
            imgW = self.aw.imgwBox.value()
            print(validate)
            print(imgH, imgW)

            train_ds = tf.keras.preprocessing.image_dataset_from_directory(
                path,
                validation_split=validate,
                subset="training",
                seed=123,
                image_size=(imgH, imgW),
                batch_size=32)

            train_ds = train_ds.unbatch()
            img = []
            lab = []

            for images, labels in train_ds:
                img.append(images.numpy().astype("uint8"))
                lab.append(labels.numpy().astype("uint8"))

            img = np.array(img, dtype="uint8")
            lab = np.array(lab, dtype="uint8")
            print(img.shape)

            val_ds = tf.keras.preprocessing.image_dataset_from_directory(
            path,
            validation_split=validate,
            subset="validation",
            seed=123,
            image_size=(imgH, imgW),
            batch_size=32)

            val_ds = val_ds.unbatch()
            img2 = []
            lab2 = []

            for images, labels in val_ds:
                img2.append(images.numpy().astype("uint8"))
                lab2.append(labels.numpy().astype("uint8"))

            img2 = np.array(img2, dtype="uint8")
            lab2 = np.array(lab2, dtype="uint8")
            print(img2.shape)
            np.savez_compressed('data.npz', train_img=img, train_lab=lab, test_img=img2, test_lab=lab2)
        else:
            print("BAD NO SUCH Path")
            self.warning.setText("BAD FOR NO SUCH PATH")
            self.warning.setIcon(QMessageBox.Icon.Warning)
            self.warning.setWindowTitle("YOU R BAD")
            self.warning.show()
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

class Thread(QThread):
    _signal = pyqtSignal(int)
    _signal2 = pyqtSignal(int)

    def __init__(self, aw, imgw):
        super(Thread, self).__init__()
        self.aw = aw
        self.imgw = imgw

    def run(self):
        path = pathlib.Path(self.imgw.filePathEdit.text())
        print(path)

        img_cnt = len(list(path.glob('*/*.*')))
        validate = self.aw.validsplitBox.value()
        imgH = self.aw.imghBox.value()
        imgW = self.aw.imgwBox.value()
        print(validate)
        print(imgH, imgW)

        if img_cnt*validate < 1:
            self._signal2.emit(-1)
        else:
            self._signal2.emit(img_cnt*(1-validate))
            self.aw.progressBar.setVisible(True)
            train_ds = tf.keras.preprocessing.image_dataset_from_directory(
                path,
                validation_split=validate,
                subset="training",
                seed=123,
                image_size=(imgH, imgW),
                batch_size=32)

            for i in range(20):
                time.sleep(0.01)
                self._signal.emit(i)

            train_ds = train_ds.unbatch()

            for i in range(20, 40):
                time.sleep(0.01)
                self._signal.emit(i)

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

            for i in range(40, 60):
                time.sleep(0.01)
                self._signal.emit(i)

            val_ds = val_ds.unbatch()

            for i in range(60, 80):
                time.sleep(0.01)
                self._signal.emit(i)

            img2 = []
            lab2 = []

            for images, labels in val_ds:
                img2.append(images.numpy().astype("uint8"))
                lab2.append(labels.numpy().astype("uint8"))

            img2 = np.array(img2, dtype="uint8")
            lab2 = np.array(lab2, dtype="uint8")
            print(img2.shape)

            for i in range(80, 100):
                time.sleep(0.01)
                self._signal.emit(i)

            np.savez_compressed('data.npz', train_img=img,
                                train_lab=lab, test_img=img2, test_lab=lab2)
            self._signal.emit(100)


class AttributeWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super(AttributeWidget, self).__init__(*args, **kwargs)

        self.vlayout = QVBoxLayout()
        self.vlayout.addStretch()

        self.validsplitLabel = QLabel("Percentage for validation: ")
        self.validsplitLabel.setFont(QFont("Consolas", 15))
        self.vlayout.addWidget(self.validsplitLabel)

        self.validsplitBox = QDoubleSpinBox()
        self.validsplitBox.setRange(0.01, 1.0)
        self.validsplitBox.setSingleStep(0.01)
        self.vlayout.addWidget(self.validsplitBox)

        self.imgsizeLabel = QLabel("Image setting: ")
        self.imgsizeLabel.setFont(QFont("Consolas", 15))
        self.vlayout.addWidget(self.imgsizeLabel)

        self.imgboxLayout = QHBoxLayout()

        self.imghvLayout = QVBoxLayout()
        self.imghLabel = QLabel("height")
        self.imghLabel.setFont(QFont("Consolas", 10))
        self.imghvLayout.addWidget(self.imghLabel)

        self.imghBox = QSpinBox()
        self.imghBox.setRange(10, 1000)
        self.imghBox.setSingleStep(10)
        self.imghvLayout.addWidget(self.imghBox)

        self.imgboxLayout.addLayout(self.imghvLayout)

        self.imgwvLayout = QVBoxLayout()
        self.imgwLabel = QLabel("width")
        self.imgwLabel.setFont(QFont("Consolas", 10))
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
        self.progressBar.setObjectName("input_prob")
        self.vlayout.addWidget(self.progressBar)
        self.progressBar.setValue(0)
        self.progressBar.setVisible(False)

        with open("./stylesheet/input.qss", "r") as f:    
            self.setStyleSheet(f.read())
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
        self.imgLabel.setFont(QFont("Consolas", 15))
        self.vlayout.addWidget(self.imgLabel)

        self.vlayout.addLayout(self.hlayout)

        with open("./stylesheet/input.qss", "r") as f:    
            self.setStyleSheet(f.read())
        self.vlayout.addStretch()
        self.setLayout(self.vlayout)


class InputWidget(QWidget):
    img_total_signal = pyqtSignal(int)

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
            self.thread = Thread(self.aw, self.imgw)
            self.thread._signal.connect(self.signal_accept)
            self.thread._signal2.connect(self.signal_warning_get)
            self.thread.start()
            self.aw.confirmBtn.setEnabled(False)

        else:
            print("BAD NO SUCH Path")
            self.warning.setText("Path not exists, please try again")
            self.warning.setIcon(QMessageBox.Icon.Warning)
            self.warning.setWindowTitle("Path Not Found")
            self.warning.show()

    def signal_accept(self, msg):
        self.aw.progressBar.setValue(int(msg))
        if self.aw.progressBar.value() == 100:
            self.aw.confirmBtn.setEnabled(True)

    def signal_warning_get(self, msg):
        if msg == -1:
            self.warning.setText(
                "Number of validation must be higher than zero img")
            self.warning.setIcon(QMessageBox.Icon.Warning)
            self.warning.setWindowTitle("Image Counts Error")
            self.warning.setDetailedText("You must choose the path containing more images.\nThat is, given images counts is too low.")
            self.warning.show()
            self.aw.confirmBtn.setEnabled(True)
        else:
            self.img_total_signal.emit(msg)

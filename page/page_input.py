import os
import pathlib
import PIL
import PIL.Image
import numpy as np
import tensorflow as tf
from PyQt5 import QtWidgets, QtCore, QtGui, QtMultimedia
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import time
from PyQt5.QtCore import QThread, pyqtSignal

ICON_SIZE = 100

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


class StyledItemDelegate(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        option.text = option.fontMetrics.elidedText(
            index.data(), QtCore.Qt.ElideRight, ICON_SIZE
        )


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
        self.imghLabel = QLabel("Height")
        self.imghLabel.setFont(QFont("Consolas", 12))
        self.imghvLayout.addWidget(self.imghLabel)

        self.imghBox = QSpinBox()
        self.imghBox.setRange(10, 1000)
        self.imghBox.setSingleStep(10)
        self.imghvLayout.addWidget(self.imghBox)

        self.imgboxLayout.addLayout(self.imghvLayout)

        self.imgwvLayout = QVBoxLayout()
        self.imgwLabel = QLabel("Width")
        self.imgwLabel.setFont(QFont("Consolas", 12))
        self.imgwvLayout.addWidget(self.imgwLabel)

        self.imgwBox = QSpinBox()
        self.imgwBox.setRange(10, 1000)
        self.imgwBox.setSingleStep(10)
        self.imgwvLayout.addWidget(self.imgwBox)

        self.imgboxLayout.addLayout(self.imgwvLayout)

        self.vlayout.addLayout(self.imgboxLayout)

        self.rgbhlayout = QHBoxLayout()
        self.rgbLabel = QLabel("color:")
        self.rgbLabel.setFont(QFont("Consolas", 12))
        self.rgbLabel.setAlignment(Qt.AlignCenter)
        self.rgbhlayout.addWidget(self.rgbLabel)

        self.rgbSelect = QComboBox()
        rgb = ["Grayscale", "RGB"]
        self.rgbSelect.addItems(rgb)
        self.rgbhlayout.addWidget(self.rgbSelect)

        self.vlayout.addLayout(self.rgbhlayout)

        self.confirmBtn = QPushButton('Confirm')
        self.vlayout.addWidget(self.confirmBtn)

        self.progressBar = QProgressBar()
        self.progressBar.setObjectName("input_prob")
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
        self.imgLabel.setFont(QFont("Consolas", 15))
        # self.vlayout.addWidget(self.imgLabel)
        self.vlayout.addWidget(self.imgLabel)

        # self.pixmap_lw = QtWidgets.QListWidget(
        #     viewMode=QtWidgets.QListView.IconMode,
        #     iconSize=ICON_SIZE * QtCore.QSize(1, 1),
        #     movement=QtWidgets.QListView.Static,
        #     resizeMode=QtWidgets.QListView.Adjust,
        # )

        # delegate = StyledItemDelegate(self.pixmap_lw)
        # self.pixmap_lw.setItemDelegate(delegate)

        # self.timer_loading = QtCore.QTimer(interval=50, timeout=self.load_image)
        # self.filenames_iterator = None

        # self.vlayout.addWidget(self.pixmap_lw)

        self.vlayout.addLayout(self.hlayout)

        self.vlayout.addStretch()
        self.setLayout(self.vlayout)


class InputWidget(QWidget):
    img_total_signal = pyqtSignal(int)
    img_size_signal = pyqtSignal(int, int, int)

    def __init__(self, *args, **kwargs):
        super(InputWidget, self).__init__(*args, **kwargs)
        self.hlayout = QHBoxLayout()
        self.hlayout.addStretch(1)

        self.himgw = QVBoxLayout()
        self.imgw = ImgWidget()
        self.himgw.addWidget(self.imgw)
        # self.hlayout.addWidget(self.imgw)

        # self.pixmap_lw = QtWidgets.QListWidget(
        #     viewMode=QtWidgets.QListView.IconMode,
        #     iconSize=ICON_SIZE * QtCore.QSize(1, 1),
        #     movement=QtWidgets.QListView.Static,
        #     resizeMode=QtWidgets.QListView.Adjust,
        # )

        # delegate = StyledItemDelegate(self.pixmap_lw)
        # self.pixmap_lw.setItemDelegate(delegate)

        # self.timer_loading = QtCore.QTimer(
        #     interval=50, timeout=self.load_image)
        # self.filenames_iterator = None

        # self.himgw.addWidget(self.pixmap_lw)
        self.hlayout.addLayout(self.himgw)

        self.hlayout.addStretch(1)
        self.aw = AttributeWidget()
        self.hlayout.addWidget(self.aw)

        self.setLayout(self.hlayout)
        self.imgw.selectFileBtn.clicked.connect(self.input_Btn)
        self.aw.confirmBtn.clicked.connect(self.confirm_Btn)

        self.warning = QMessageBox()

        with open("./stylesheet/input.qss", "r") as f:
            self.setStyleSheet(f.read())

    def PlaySound(self):
        audio_url = QtCore.QUrl.fromLocalFile("./sound/button.wav")
        audio_content = QtMultimedia.QMediaContent(audio_url)
        self.player = QtMultimedia.QMediaPlayer()
        self.player.setVolume(50.0)
        self.player.setMedia(audio_content)
        self.player.play()

    def input_Btn(self):
        self.PlaySound()
        print("open folder")
        folder_path = QFileDialog.getExistingDirectory(
            self, "Open folder", "./")  # start path

        # if folder_path:
        #     self.start_loading(folder_path)

        self.imgw.filePathEdit.setText(folder_path)
        folder_path = pathlib.Path(folder_path)
        print(folder_path)

        img_cnt = len(list(folder_path.glob('*/*.*')))
        print(img_cnt)
        # roses = list(folder_path.glob('roses/*'))
        # x = PIL.Image.open(str(roses[0]))
        # x.show()

        # directory = QtWidgets.QFileDialog.getExistingDirectory(
        #     options=QtWidgets.QFileDialog.DontUseNativeDialog
        # )
        # if directory:
        #     self.start_loading(directory)

    def confirm_Btn(self):
        self.PlaySound()
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

    def start_loading(self, directory):
        if self.timer_loading.isActive():
            self.timer_loading.stop()
        # self.path_le.setText(directory)
        self.filenames_iterator = self.load_images(directory)
        self.pixmap_lw.clear()
        self.timer_loading.start()

    # @QtCore.pyqtSlot()
    def load_image(self):
        try:
            filename = next(self.filenames_iterator)
        except StopIteration:
            self.timer_loading.stop()
        else:
            name = os.path.basename(filename)
            it = QtWidgets.QListWidgetItem(name)
            it.setIcon(QtGui.QIcon(filename))
            self.pixmap_lw.addItem(it)

    def load_images(self, directory):
        it = QtCore.QDirIterator(
            directory,
            ["*.jpg", "*.png"],
            QtCore.QDir.Files,
            QtCore.QDirIterator.Subdirectories,
        )
        while it.hasNext():
            filename = it.next()
            yield filename

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
            self.warning.setDetailedText(
                "You must choose the path containing more images.\nThat is, given images counts is too low.")
            self.warning.show()
            self.aw.confirmBtn.setEnabled(True)
        else:
            self.img_total_signal.emit(msg)
            color = 0
            if self.aw.rgbSelect.currentIndex() == 0:
                color = 1
            else:
                color = 3
            self.img_size_signal.emit(self.aw.imghBox.value(
            ), self.aw.imgwBox.value(), color)

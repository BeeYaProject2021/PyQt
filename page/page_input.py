import os
import random
import pathlib
import numpy as np
import tensorflow as tf
from PyQt5 import QtWidgets, QtCore, QtGui, QtMultimedia
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import time
from PyQt5.QtCore import QThread, pyqtSignal

ICON_SIZE = 100
imgH = 100
imgW = 100
imgC = 0


class Thread(QThread):
    _signal = pyqtSignal(int)
    _signal2 = pyqtSignal(int)

    def __init__(self, aw, imgw, color, saveFilePath):
        super(Thread, self).__init__()
        self.aw = aw
        self.imgw = imgw
        self.color = color
        self.saveFilePath = saveFilePath

    def run(self):
        global imgH
        global imgW
        global imgC
        path = pathlib.Path(self.imgw.filePathEdit.text())
        print(path)

        img_cnt = len(list(path.glob('*/*.*')))
        validate = self.aw.validsplitBox.value()
        imgH = self.aw.imghBox.value()
        imgW = self.aw.imgwBox.value()
        imgC = self.color
        print(validate)
        print(imgH, imgW)

        if img_cnt*validate < 1:
            self._signal2.emit(-1)
        else:
            self.aw.progressBar.setVisible(True)

            train_ds = tf.keras.preprocessing.image_dataset_from_directory(
                path,
                validation_split=validate,
                subset="training",
                seed=123,
                image_size=(imgH, imgW),
                color_mode='grayscale' if self.color == 1 else 'rgb',
                batch_size=32)

            class_names = train_ds.class_names
            print(class_names)

            img_cnt = len(np.concatenate([i for x, i in train_ds], axis=0))
            self._signal2.emit(img_cnt)

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
                color_mode='grayscale' if self.color == 1 else 'rgb',
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

            np.savez_compressed(str(self.saveFilePath), train_img=img,
                                train_lab=lab, test_img=img2, test_lab=lab2)
            print(str(self.saveFilePath))
            store_class = str(self.saveFilePath) + ".txt"
            with open(store_class, "w") as f:
                for i in class_names:
                    f.writelines(i + "\n")

            store_class = "default/0.txt"
            with open(store_class, "w") as f:
                for i in class_names:
                    f.writelines(i + "\n")
            # np.savez_compressed('data.npz', train_img=img,
            #                     train_lab=lab, test_img=img2, test_lab=lab2)
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
        self.imghLabel.setFont(QFont("Consolas", 15))
        self.imghvLayout.addWidget(self.imghLabel)

        self.imghBox = QSpinBox()
        self.imghBox.setRange(10, 1000)
        self.imghBox.setSingleStep(10)
        self.imghvLayout.addWidget(self.imghBox)

        self.imgboxLayout.addLayout(self.imghvLayout)

        self.imgwvLayout = QVBoxLayout()
        self.imgwLabel = QLabel("Width")
        self.imgwLabel.setFont(QFont("Consolas", 15))
        self.imgwvLayout.addWidget(self.imgwLabel)

        self.imgwBox = QSpinBox()
        self.imgwBox.setRange(10, 1000)
        self.imgwBox.setSingleStep(10)
        self.imgwvLayout.addWidget(self.imgwBox)

        self.imgboxLayout.addLayout(self.imgwvLayout)

        self.vlayout.addLayout(self.imgboxLayout)

        self.rgbhlayout = QHBoxLayout()
        self.rgbLabel = QLabel("Color mode:")
        self.rgbLabel.setFont(QFont("Consolas", 15))
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
        self.hlayout.addStretch()

        self.filePathEdit = QLabel()
        self.filePathEdit.setFixedWidth(440)
        self.filePathEdit.setObjectName("Path")
        self.hlayout.addWidget(self.filePathEdit)

        self.selectFileBtn = QPushButton('Select')
        self.hlayout.addWidget(self.selectFileBtn)

        self.vlayout = QVBoxLayout()
        # self.vlayout.addStretch()
        self.hlayout2 = QHBoxLayout()
        self.hlayout2.addStretch()
        self.imgLabel = QLabel('Select a folder path for input dataset')
        self.imgLabel.setFont(QFont("Consolas", 15))
        self.hlayout2.addWidget(self.imgLabel)
        self.hlayout2.addStretch()
        self.vlayout.addLayout(self.hlayout2)

        self.hlayout.addStretch()
        self.vlayout.addLayout(self.hlayout)

        # self.vlayout.addStretch()
        self.setLayout(self.vlayout)


class ImgDisplay(QWidget):
    def __init__(self, path, label):
        super(ImgDisplay, self).__init__()
        self.vlayout = QVBoxLayout()

        self.img = QLabel()
        self.imgPixmap = QPixmap(path)
        self.imgPixmap = self.imgPixmap.scaled(100, 100)
        self.img.setPixmap(self.imgPixmap)
        self.img.setMaximumSize(100, 100)
        # self.img.setFixedSize(100, 100)
        self.vlayout.addWidget(self.img)

        self.imgLabel = QLabel()
        self.imgLabel.setFont(QFont("Consolas", 8))
        self.imgLabel.setText(label)

        self.vlayout.addWidget(self.imgLabel)
        self.setLayout(self.vlayout)


class InputWidget(QWidget):
    img_total_signal = pyqtSignal(int)
    img_size_signal = pyqtSignal(int, int, int)
    imgTuples = []

    def __init__(self, *args, **kwargs):
        super(InputWidget, self).__init__(*args, **kwargs)
        self.hlayout = QHBoxLayout()
        self.hlayout.addStretch()

        self.vimgw = QVBoxLayout()
        self.vimgw.addStretch()
        self.imgw = ImgWidget()
        self.vimgw.addWidget(self.imgw)

        self.imgPage = QComboBox()
        self.imgPage.setEnabled(False)
        self.imgPage.addItem("0")
        self.imgPage.currentIndexChanged.connect(self.PageChange)
        self.vimgw.addWidget(self.imgPage)

        self.imgGridLayout = QGridLayout()
        self.vimgw.addLayout(self.imgGridLayout)

        self.vimgw.addStretch()
        self.hlayout.addLayout(self.vimgw)

        self.hlayout.addStretch()
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
        self.player.setVolume(25.0)
        self.player.setMedia(audio_content)
        self.player.play()

    def input_Btn(self):
        self.PlaySound()
        self.imgTuples.clear()
        print("open folder")
        folder_path = QFileDialog.getExistingDirectory(
            self, "Open folder", "C:/")  # start path

        self.imgw.filePathEdit.setText(folder_path)
        if os.path.exists(self.imgw.filePathEdit.text()):
            folder_path = pathlib.Path(folder_path)
            print(folder_path)

            imgclass = []
            labelPath = list(folder_path.glob('*'))
            for i in range(len(labelPath)):
                if labelPath[i].is_dir():
                    imgclass.append(labelPath[i])
                    label = labelPath[i].relative_to(folder_path)
                    print(label)
                    img = list(labelPath[i].glob('*'))
                    for j in range(len(img)):
                        self.imgTuples.append((img[j], label))
                    print(len(img))
            random.shuffle(self.imgTuples)
            self.imgPage.setEnabled(True)
            self.imgPage.clear()
            # print(int((len(self.imgTuples)-1)/20))

            for i in range(int((len(self.imgTuples)-1)/20)+1):
                self.imgPage.addItem(str(i+1))
            for i in range(4):
                for j in range(5):
                    num = i*5+j
                    if self.imgGridLayout.itemAtPosition(i, j) is not None:
                        self.imgGridLayout.removeWidget(
                            self.imgGridLayout.itemAtPosition(i, j).widget())
                    self.imgGridLayout.addWidget(
                        ImgDisplay(str(self.imgTuples[num][0]), str(self.imgTuples[num][1])), i, j)

            print('---')
            print(len(self.imgTuples))
            print('---')
            print(imgclass)

            img_cnt = len(list(folder_path.glob('*/*.*')))
            print(img_cnt)
        else:
            self.imgPage.setEnabled(False)
            self.imgPage.clear()
            self.imgPage.addItem("0")
            for i in range(4):
                for j in range(5):
                    if self.imgGridLayout.itemAtPosition(i, j) is not None:
                        self.imgGridLayout.removeWidget(
                            self.imgGridLayout.itemAtPosition(i, j).widget())

    def PageChange(self, index):
        # print(index)
        if self.imgPage.isEnabled():
            for i in range(4):
                for j in range(5):
                    num = i*5+j+index*20
                    # print(num)
                    if self.imgGridLayout.itemAtPosition(i, j) is not None:
                        self.imgGridLayout.removeWidget(
                            self.imgGridLayout.itemAtPosition(i, j).widget())
                    if num < len(self.imgTuples):
                        self.imgGridLayout.addWidget(
                            ImgDisplay(str(self.imgTuples[num][0]), str(self.imgTuples[num][1])), i, j)

    def confirm_Btn(self):
        # Check Path exists
        if os.path.exists(self.imgw.filePathEdit.text()):
            self.color = 0
            if self.aw.rgbSelect.currentIndex() == 0:
                self.color = 1
            else:
                self.color = 3
            self.PlaySound()
            saveFilePath = QFileDialog.getSaveFileName(
                self, "Save .npz file", "./untitle.npz", "*.npz")
            print("HI")
            print(saveFilePath)
            print("HI")
            if saveFilePath[0] != "":
                self.thread = Thread(self.aw, self.imgw,
                                     self.color, saveFilePath[0])
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
            self.img_size_signal.emit(self.aw.imghBox.value(
            ), self.aw.imgwBox.value(), self.color)

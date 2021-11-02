import sys
from typing import Optional
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QDialog, QListWidget, QAbstractItemView, QListWidgetItem
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QDragMoveEvent, QMouseEvent, QPixmap, QKeyEvent
from PyQt5.QtCore import Qt, QModelIndex


class MyListWidget(QListWidget):
    """支持拖拽的QListWidget"""
    def __init__(self, parent: Optional[QWidget]=None) -> None:
        super().__init__(parent)
        # 拖拽设置
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDragDropMode(QAbstractItemView.DragDrop)            # 设置拖放
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)  # 设置选择多个
        self.setDefaultDropAction(Qt.CopyAction)
        # 双击可编辑
        self.edited_item = self.currentItem()
        self.close_flag = True
        self.doubleClicked.connect(self.item_double_clicked)
        self.currentItemChanged.connect(self.close_edit)
    
    def keyPressEvent(self, e: QKeyEvent) -> None:
        """回车事件，关闭edit"""
        super().keyPressEvent(e)
        if e.key() == Qt.Key_Return:
            if self.close_flag:
                self.close_edit()
            self.close_flag = True

    def edit_new_item(self) -> None:
        """edit一个新的item"""
        self.close_flag = False
        self.close_edit()
        count = self.count()
        self.addItem('')
        item = self.item(count)
        self.edited_item = item
        self.openPersistentEditor(item)
        self.editItem(item)

    def item_double_clicked(self, modelindex: QModelIndex) -> None:
        """双击事件"""
        self.close_edit()
        item = self.item(modelindex.row())
        self.edited_item = item
        self.openPersistentEditor(item)
        self.editItem(item)
    
    def close_edit(self, *_) -> None:
        """关闭edit"""
        if self.edited_item and self.isPersistentEditorOpen(self.edited_item):
            self.closePersistentEditor(self.edited_item)

    def dragEnterEvent(self, e: QDragEnterEvent) -> None:
        """（从外部或内部控件）拖拽进入后触发的事件"""
        # print(e.mimeData().text())
        if e.mimeData().hasText():
            if e.mimeData().text().startswith('file:///'):
                e.accept()
        else:
            e.ignore()

    def dragMoveEvent(self, e: QDragMoveEvent) -> None:
        """拖拽移动过程中触发的事件"""
        e.accept()

    def dropEvent(self, e: QDropEvent) -> None:
        """拖拽结束以后触发的事件"""
        paths = e.mimeData().text().split('\n')
        for path in paths:
            path = path.strip()
            if len(path) > 8:
                self.addItem(path.strip()[8:])
        e.accept()

class MyLabel(QLabel):
    """可接收拖拽的Label"""
    def __init__(self, parent: Optional[QWidget]=None) -> None:
        super().__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e: QDragEnterEvent) -> None:
        e.setDropAction(Qt.MoveAction)
        e.accept()

    # def dragMoveEvent(self, e: QDragMoveEvent) -> None:
    #     e.setDropAction(Qt.MoveAction)
    #     e.accept()

    def dropEvent(self, e: QDropEvent) -> None:
        e.setDropAction(Qt.MoveAction)
        e.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = QWidget()

    labelw = MyLabel()
    labelw.setAlignment(Qt.AlignCenter)
    labelw.setPixmap(QPixmap('image.jpg'))
    listw = MyListWidget()
    
    layout = QVBoxLayout()
    layout.addWidget(labelw)
    layout.addWidget(listw)
    main_window.setLayout(layout)
    
    main_window.setWindowTitle("test")
    main_window.show()
    sys.exit(app.exec_())



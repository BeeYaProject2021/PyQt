import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class GraphicsScene(QGraphicsScene):
    nodes = []
    edges = []
    show_attribute_signal = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

    def sendMsg(self, id):
        if len(self.selectedItems()) == 1:
            print("only 1")
            if isinstance(self.selectedItems()[0], NodeItem or QGraphicsTextItem):
                print("correct obj")
                self.show_attribute_signal.emit(id-1)

    def addNode(self, id, pos):
        index = len(self.nodes)
        node = NodeItem(index, id)
        self.nodes.append(node)
        self.nodes[index].setPos(pos)
        self.addItem(self.nodes[index])

    def addEdge(self, start_node, end_node):
        index = len(self.edges)
        start_node.connected = True
        end_node.connected = True
        edge = GraphicsPathItem(index, start_node, end_node)
        self.edges.append(edge)
        self.addItem(self.edges[index])
        self.edges[index].setEdge()

    def removeNode(self, node):
        for edge in self.edges:
            if edge.start_node.index == node.index:
                self.nodes[edge.end_node.index].leftPort.connected = False
                self.removeItem(edge)
                self.edges.remove(edge)
        for edge in self.edges:
            if edge.end_node.index == node.index:
                self.nodes[edge.start_node.index].rightPort.connected = False
                self.removeItem(edge)
                self.edges.remove(edge)
        self.removeItem(node)
        self.nodes.remove(node)
        self.updateNode()
        self.updateEdge()

    def removeEdge(self, edge):
        self.nodes[edge.end_node.index].leftPort.connected = False
        self.nodes[edge.start_node.index].rightPort.connected = False
        self.removeItem(edge)
        self.edges.remove(edge)
        self.updateEdge()

    def updateNode(self):
        for node in self.nodes:
            for edge in self.edges:
                if edge.start_node.index == node.index:
                    edge.start_node.index = self.nodes.index(node)
                if edge.end_node.index == node.index:
                    edge.end_node.index = self.nodes.index(node)
            node.index = self.nodes.index(node)
            node.leftPort.index = node.index
            node.rightPort.index = node.index
            node.text.setText("Node"+str(node.index)+", "+str(node.id))

    def updateEdge(self):
        for edge in self.edges:
            edge.index = self.edges.index(edge)


class GraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setAcceptDrops(True)
        self.setMouseTracking(True)
        self.setRenderHints(QPainter.Antialiasing |
                            QPainter.HighQualityAntialiasing |
                            QPainter.TextAntialiasing |
                            QPainter.SmoothPixmapTransform |
                            QPainter.LosslessImageRendering)
        self.graphics_scene = GraphicsScene(self)
        self.setScene(self.graphics_scene)

        self.drag_edge = False

        # self.setDragMode(self.RubberBandDrag)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        # self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        # self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

    def getClickedItem(self, pos):
        return self.itemAt(pos)

    def mousePressEvent(self, e):
        super().mousePressEvent(e)
        if e.buttons() == Qt.RightButton:
            item = self.getClickedItem(e.pos())
            if isinstance(item, PortItem):
                if item.id == 1 and item.connected == False:
                    self.start_item = item
                    self.end = self.mapToScene(e.pos())
                    self.fake_edge = GraphicsPathItem(-1,
                                                      self.start_item, self.end)
                    self.fake_edge.start(self.start_item.pos(
                    )+QPointF(self.start_item.rect().width()/2, self.start_item.rect().height()/2)+self.graphics_scene.nodes[self.start_item.index].pos())
                    self.graphics_scene.addItem(self.fake_edge)
                    self.drag_edge = True

    def mouseMoveEvent(self, e):
        super().mouseMoveEvent(e)
        if e.buttons() == Qt.RightButton and self.drag_edge:
            self.end = self.mapToScene(e.pos())
            self.fake_edge.end_node = self.end
            self.fake_edge.setEdge()
            # self.fake_edge.edge_path.clear()

    def mouseReleaseEvent(self, e):
        if self.drag_edge:
            item = self.getClickedItem(e.pos()+QPoint(3, 0))
            item1 = self.getClickedItem(e.pos()+QPoint(-3, 0))
            if isinstance(item, PortItem):
                if item.index != self.start_item.index and item.id == 0 and item.connected == False:
                    self.graphics_scene.addEdge(self.start_item, item)
            elif isinstance(item1, PortItem):
                if item1.index != self.start_item.index and item1.id == 0 and item1.connected == False:
                    self.graphics_scene.addEdge(self.start_item, item1)

            self.graphics_scene.removeItem(self.fake_edge)
            self.fake_edge = None
            self.drag_edge = False
        else:
            super().mouseReleaseEvent(e)

    def dragEnterEvent(self, e):
        e.accept()

    def dragMoveEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        if e.mimeData().text() == "conv2D":
            e.accept()
            self.graphics_scene.addNode(
                1, (self.mapToScene(e.pos())).toPoint())
        elif e.mimeData().text() == "maxpooling2D":
            e.accept()
            self.graphics_scene.addNode(
                2, (self.mapToScene(e.pos())).toPoint())
        elif e.mimeData().text() == "flatten":
            e.accept()
            self.graphics_scene.addNode(
                3, (self.mapToScene(e.pos())).toPoint())
        elif e.mimeData().text() == "dense":
            e.accept()
            self.graphics_scene.addNode(
                4, (self.mapToScene(e.pos())).toPoint())


class GraphicsPathItem(QGraphicsPathItem):
    def __init__(self, index, start_node, end_node, parent=None):
        super().__init__(parent)
        self.index = index
        self.start_node = start_node
        self.end_node = end_node
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsFocusable, True)
        pen = QPen()
        pen.setColor(Qt.black)
        pen.setWidth(2)
        self.setPen(pen)

        self.edge_path = QPainterPath()

    def start(self, pos):
        self.edge_path.moveTo(pos)

    def setEdge(self):
        start_pos = self.start_node.pos(
        )+QPointF(self.start_node.rect().width()/2, self.start_node.rect().height()/2)+self.scene().nodes[self.start_node.index].pos()
        end_pos = QPointF()
        if isinstance(self.end_node, PortItem):
            end_pos = self.end_node.pos(
            )+QPointF(self.end_node.rect().width()/2, self.end_node.rect().height()/2)+self.scene().nodes[self.end_node.index].pos()
        else:
            end_pos = self.end_node
        mid_pos = (start_pos+end_pos)/2
        self.edge_path.moveTo(start_pos)
        self.edge_path.cubicTo(
            QPointF(mid_pos.x(), start_pos.y()), mid_pos, end_pos)
        self.setPath(self.edge_path)
        self.edge_path.clear()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key.Key_Delete:
            self.scene().removeEdge(self)


class NodeItem(QGraphicsRectItem):

    def __init__(self, index, id, parent=None):
        super().__init__(parent)
        self.index = index
        self.id = id
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(
            QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsFocusable, True)
        self.width = 150
        self.height = 50
        self.setRect(0, 0, self.width, self.height)
        self.setBrush(QColor(0xaa, 0xaa, 0xaa, 0xaa))

        self.text = QGraphicsSimpleTextItem(
            "Node"+str(self.index)+", "+str(self.id), self)
        self.text.setPos(self.width/2-self.text.boundingRect().width()/2,
                         self.height/2-self.text.boundingRect().height()/2)
        self.text.setBrush(QColor(255, 0, 0))

        self.leftPort = PortItem(self.index, 0, self)
        self.leftPort.setPos(5, self.height/2.7)
        self.rightPort = PortItem(self.index, 1, self)
        self.rightPort.setPos(self.width-20, self.height/2.7)

    def mousePressEvent(self, e):
        super().mousePressEvent(e)
        if self.isSelected():
            self.scene().sendMsg(self.id)

    def mouseMoveEvent(self, e):
        super().mouseMoveEvent(e)
        if self.isSelected():
            for edge in self.scene().edges:
                edge.setEdge()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key.Key_Delete:
            self.scene().removeNode(self)


class PortItem(QGraphicsEllipseItem):
    connected = False

    def __init__(self, index, id, parent=None):
        super(PortItem, self).__init__(parent)
        self.index = index
        self.id = id
        self.portDiam = 20
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setBrush(QColor(0x00, 0xaa, 0x00, 0x66))
        self.setRect(0, 0, self.portDiam, self.portDiam)


class ViewWidget(QWidget):

    central_widget = None
    layout_container = None

    def __init__(self):
        super(ViewWidget, self).__init__()
        # self.central_widget = QWidget()
        self.vlayout = QVBoxLayout()
        self.setLayout(self.vlayout)
        # self.setCentralWidget(self.central_widget)
        self.gv = GraphicsView(self)
        self.vlayout.addWidget(self.gv)
        self.toggle_btn = QPushButton("Toggle Drag Mode")
        self.toggle_btn.clicked.connect(self.toggle_drag_mode)
        self.vlayout.addWidget(self.toggle_btn)
        self.resize(1280, 720)

    def toggle_drag_mode(self):
        if self.gv.dragMode() == QGraphicsView.ScrollHandDrag:
            self.gv.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        else:
            self.gv.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)

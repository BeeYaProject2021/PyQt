import sys
from PyQt5 import QtWidgets, QtCore, QtGui


class CustomItem(QtWidgets.QGraphicsItem):
    def __init__(self, pointONLeft=False, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ellipseOnLeft = pointONLeft
        self.point = None
        self.endPoint =None

        self.isStart = None

        self.line = None

        self.setAcceptHoverEvents(True)
        self.setFlag(self.ItemIsMovable)
        self.setFlag(self.ItemSendsGeometryChanges)

    def addLine(self, line, ispoint):
        if not self.line:
            self.line = line
            self.isStart = ispoint

    def itemChange(self, change, value):

        if change == self.ItemPositionChange and self.scene():
            self.moveLineToCenter(value)

        return super(CustomItem, self).itemChange(change, value)

    def moveLineToCenter(self, newPos): # moves line to center of the ellipse

        if self.line:

            if self.ellipseOnLeft:
                xOffset = QtCore.QRectF(-5, 30, 10, 10).x() + 5
                yOffset = QtCore.QRectF(-5, 30, 10, 10).y() + 5

            else:
                xOffset = QtCore.QRectF(95, 30, 10, 10).x() + 5
                yOffset = QtCore.QRectF(95, 30, 10, 10).y() + 5

            newCenterPos = QtCore.QPointF(newPos.x() + xOffset, newPos.y() + yOffset)

            p1 = newCenterPos if self.isStart else self.line.line().p1()
            p2 =  self.line.line().p2() if self.isStart else newCenterPos

            self.line.setLine(QtCore.QLineF(p1, p2))

    def containsPoint(self, pos):  # checks whether the mouse is inside the ellipse
        x = self.mapToScene(QtCore.QRectF(-5, 30, 10, 10).adjusted(-0.5, 0.5, 0.5, 0.5)).containsPoint(pos, QtCore.Qt.OddEvenFill) or \
            self.mapToScene(QtCore.QRectF(95, 30, 10, 10).adjusted(0.5, 0.5, 0.5, 0.5)).containsPoint(pos,
                                                                                                      QtCore.Qt.OddEvenFill)

        return x

    def boundingRect(self):
        return QtCore.QRectF(-5, 0, 110, 110)

    def paint(self, painter, option, widget):

        pen = QtGui.QPen(QtCore.Qt.red)
        pen.setWidth(2)

        painter.setPen(pen)

        painter.setBrush(QtGui.QBrush(QtGui.QColor(31, 176, 224)))
        painter.drawRoundedRect(QtCore.QRectF(0, 0, 100, 100), 4, 4)

        painter.setBrush(QtGui.QBrush(QtGui.QColor(214, 13, 36)))

        if self.ellipseOnLeft: # draws ellipse on left
            painter.drawEllipse(QtCore.QRectF(-5, 30, 10, 10))

        else: # draws ellipse on right
            painter.drawEllipse(QtCore.QRectF(95, 30, 10, 10))


# ------------------------Scene Class ----------------------------------- #
class Scene(QtWidgets.QGraphicsScene):
    def __init__(self):
        super(Scene, self).__init__()
        self.startPoint = None
        self.endPoint = None

        self.line = None
        self.graphics_line = None

        self.item1 = None
        self.item2 = None

    def mousePressEvent(self, event):
        self.line = None
        self.graphics_line = None

        self.item1 = None
        self.item2 = None

        self.startPoint = None
        self.endPoint = None

        if self.itemAt(event.scenePos(), QtGui.QTransform()) and isinstance(self.itemAt(event.scenePos(),
                                                                            QtGui.QTransform()), CustomItem):

            self.item1 = self.itemAt(event.scenePos(), QtGui.QTransform())
            self.checkPoint1(event.scenePos())

            if self.startPoint:
                self.line = QtCore.QLineF(self.startPoint, self.endPoint)
                self.graphics_line = self.addLine(self.line)

                self.update_path()

        super(Scene, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):

        if event.buttons() & QtCore.Qt.LeftButton and self.startPoint:
            self.endPoint = event.scenePos()
            self.update_path()

        super(Scene, self).mouseMoveEvent(event)

    def filterCollidingItems(self, items):  #  filters out all the colliding items and returns only instances of CustomItem
        return [x for x in items if isinstance(x, CustomItem) and x != self.item1]

    def mouseReleaseEvent(self, event):

        if self.graphics_line:

            self.checkPoint2(event.scenePos())
            self.update_path()

            if self.item2 and not self.item1.line and not self.item2.line:
                self.item1.addLine(self.graphics_line, True)
                self.item2.addLine(self.graphics_line, False)

            else:
                if self.graphics_line:
                    self.removeItem(self.graphics_line)

        super(Scene, self).mouseReleaseEvent(event)

    def checkPoint1(self, pos):

        if self.item1.containsPoint(pos):

            self.item1.setFlag(self.item1.ItemIsMovable, False)
            self.startPoint = self.endPoint = pos

        else:
            self.item1.setFlag(self.item1.ItemIsMovable, True)

    def checkPoint2(self, pos):

        item_lst = self.filterCollidingItems(self.graphics_line.collidingItems())
        contains = False

        if not item_lst:  # checks if there are any items in the list
            return

        for self.item2 in item_lst:
            if self.item2.containsPoint(pos):
                contains = True
                self.endPoint = pos
                break
   
        if not contains:
            self.item2 = None

    def update_path(self):
        if self.startPoint and self.endPoint:
            self.line.setP2(self.endPoint)
            self.graphics_line.setLine(self.line)


def main():
    app = QtWidgets.QApplication(sys.argv)
    scene = Scene()

    item1 = CustomItem(True)
    scene.addItem(item1)

    item2 = CustomItem()
    scene.addItem(item2)

    view = QtWidgets.QGraphicsView(scene)
    view.setViewportUpdateMode(view.FullViewportUpdate)
    view.setMouseTracking(True)

    view.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

# import sys, os
# from PyQt5 import QtCore, QtGui, QtWidgets
# from PyQt5.QtCore import QObject , pyqtSignal



# can_draw=0
# start=0
# end=0
# first_connect=0
# second_connect =0


# class DragButton(QtWidgets.QPushButton):
#     connectionRequested = pyqtSignal(QtWidgets.QPushButton)
#     moved = pyqtSignal()
#     def __init__(self, title, parent=None):
#         super().__init__(title, parent)
#         self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
#         self.customContextMenuRequested.connect(self.showMenu)

#     def showMenu(self):
#         menu = QtWidgets.QMenu()
#         menu.addAction("connect", lambda: self.connectionRequested.emit(self))
#         menu.exec_(self.cursor().pos())

#     def mouseMoveEvent(self, e):
#         if e.buttons() != QtCore.Qt.LeftButton:
#             return
#         mimeData = QtCore.QMimeData()
#         drag = QtGui.QDrag(self)
#         drag.setMimeData(mimeData)
#         drag.setHotSpot(e.pos() - self.rect().topLeft())
#         dropAction = drag.exec_(QtCore.Qt.MoveAction)

#         self.moved.emit()


#     def connectLine(self):

#         global can_draw
#         global start
#         global end
#         global first_connect
#         global second_connect 

#         view = self.parent()

#         can_draw +=1

#         if can_draw == 1:


#             start = QtCore.QPointF(view.mapToScene(self.pos()))


#         if can_draw == 2:

#             end = QtCore.QPointF(view.mapToScene(self.pos()))


#             can_draw -= 2


#             view.createLineItem(start,end)

# class GraphicsLineItem(QtWidgets.QGraphicsLineItem):

#     def __init__(self, source, destination, parent=None):
#         super().__init__(parent)
#         self.source = source
#         self.destination = destination

#         self.move()

#         self.source.moved.connect(self.move)
#         self.destination.moved.connect(self.move)

#     def contextMenuEvent(self, event):
#         menu = QtWidgets.QMenu()
#         menu.addAction("Delete", self.remove)
#         menu.exec_(self.cursor().pos())
#         print(self.a)

#     def remove(self):
#         self.scene().removeItem(self)

#     def shape(self):
#         p = super(GraphicsLineItem, self).shape()
#         stroker = QtGui.QPainterPathStroker()
#         stroker.setWidth(20)
#         return stroker.createStroke(p)
    
#     def move(self):
#         self.setLine(QLineF(self.source.pos(), self.destination.pos()))



# class View(QtWidgets.QGraphicsView):
#     def __init__(self, parent=None):
#         super(View, self).__init__(parent)
#         self.setScene(QtWidgets.QGraphicsScene(self))
#         self.setAcceptDrops(True)
#         self.setSceneRect(QtCore.QRectF(self.viewport().rect()))

#         self.btn1 = QtWidgets.QPushButton("Start")
#         self.btn1.setGeometry(230, 80, 100, 30)
#         self.btn1.setCheckable(True)
#         self.btn1.clicked.connect(self.add_Text)
#         self.source = None

#     def _createLineF(self,start,end):

#         return QtCore.QLineF(start, end)



#     def clearScene(self):
#         self.scene().clear()
#         self.source = None

#     def add_Text(self):
#         button = DragButton('Text', self)
#         button.setGeometry(230, 80, 100, 30)
#         button.show() 
#         button.connectionRequested.connect(self.connectButton)

#     def connectButton(self, button):
#         # Do not connect a button with itself
#         if not self.source or button == self.source:
#             self.source = button
#             return

#         line = GraphicsLineItem(self.source, button)
#         self.scene().addItem(line)
#         self.source = None

#     def dragEnterEvent(self, e):
#         e.accept()

#     def dragMoveEvent(self, e):
#         e.accept()

#     def dropEvent(self, e):
#         btn = e.source()
#         position = e.pos()
#         btn.move(position)
#         e.setDropAction(QtCore.Qt.MoveAction)
#         e.accept()


# class Window(QtWidgets.QWidget):
#     def __init__(self, parent=None):
#         super(Window, self).__init__(parent)
#         self.view = View()
#         self.button = QtWidgets.QPushButton(
#             "Clear View", clicked=self.view.scene().clear
#         )
#         self.btn1 = QtWidgets.QPushButton("add button")
#         self.btn1.setCheckable(True)
#         self.btn1.clicked.connect(self.view.add_Text)
#         layout = QtWidgets.QVBoxLayout(self)
#         layout.addWidget(self.view)
#         layout.addWidget(self.btn1)


# if __name__ == "__main__":

#     import sys

#     app = QtWidgets.QApplication(sys.argv)
#     window = Window()
#     window.resize(640, 480)
#     window.show()
#     sys.exit(app.exec_())
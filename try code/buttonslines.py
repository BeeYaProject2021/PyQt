import sys
import math
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QGraphicsScene

from PyQt5.QtWidgets import QStyledItemDelegate

class GraphicItem(QGraphicsPixmapItem):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pix = QPixmap("image.jpg")
        self.width = 50    # 图元宽
        self.height = 50   # 图元高
        self.setPixmap(self.pix)  # 设置图元
        self.setFlag(QGraphicsItem.ItemIsSelectable)  # ***设置图元是可以被选择的
        self.setFlag(QGraphicsItem.ItemIsMovable)     # ***设置图元是可以被移动的

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        # 如果图元被选中，就更新连线，这里更新的是所有。可以优化，只更新连接在图元上的。
        if self.isSelected():
            for gr_edge in self.scene().edges:
                gr_edge.edge_wrap.update_positions()

class GraphicEdge(QGraphicsPathItem):
    def __init__(self, edge_wrap, parent=None):
        super().__init__(parent)
        # 这个参数是GraphicEdge的包装类，见下文
        self.edge_wrap = edge_wrap
        self.width = 3.0  # 线条的宽度
        self.pos_src = [0, 0]  # 线条起始位置 x，y坐标
        self.pos_dst = [0, 0]  # 线条结束位置

        self._pen = QPen(QColor("#000"))  # 画线条的
        self._pen.setWidthF(self.width)

        self._pen_dragging = QPen(QColor("#000"))  # 画拖拽线条时线条的
        self._pen_dragging.setStyle(Qt.DashDotLine)
        self._pen_dragging.setWidthF(self.width)

        self.setFlag(QGraphicsItem.ItemIsSelectable)  # 线条可选
        self.setZValue(-1)  # 让线条出现在所有图元的最下层

    def set_src(self, x, y):
        self.pos_src = [x, y]

    def set_dst(self, x, y):
        self.pos_dst = [x, y]
	
	# 计算线条的路径
    def calc_path(self):
        path = QPainterPath(QPointF(self.pos_src[0], self.pos_src[1]))  # 起点
        path.lineTo(self.pos_dst[0], self.pos_dst[1])  # 终点
        return path
	
	# override
    def boundingRect(self):
        return self.shape().boundingRect()
	
	# override
    def shape(self):
        return self.calc_path()
	
	# override
    def paint(self, painter, graphics_item, widget=None):
        self.setPath(self.calc_path()) # 设置路径
        path = self.path()
        if self.edge.end_item is None: 
        	# 包装类中存储了线条开始和结束位置的图元
        	# 刚开始拖拽线条时，并没有结束位置的图元，所以是None
        	# 这个线条画的是拖拽路径，点线
            painter.setPen(self._pen_dragging)
            painter.drawPath(path)
        else:
        	# 这画的才是连接后的线
            painter.setPen(self._pen)
            painter.drawPath(path)

class Edge:
    def __init__(self, scene, start_item, end_item):
    	# 参数分别为场景、开始图元、结束图元
        super().__init__()
        self.scene = scene
        self.start_item = start_item
        self.end_item = end_item
		
		# 线条图形在此处创建
        self.gr_edge = GraphicEdge(self)
        # 此类一旦被初始化就在添加进scene
        self.scene.add_edge(self.gr_edge)
		
		# 开始更新
        if self.start_item is not None:
            self.update_positions()
	
	# 最终保存进scene
    def store(self):
        self.scene.add_edge(self.gr_edge)
	
	# 更新位置
    def update_positions(self):
    	# src_pos 记录的是开始图元的位置，此位置为图元的左上角
        src_pos = self.start_item.pos()
        # 想让线条从图元的中心位置开始，让他们都加上偏移
        patch = self.start_item.width / 2
        self.gr_edge.set_src(src_pos.x()+patch, src_pos.y()+patch)
        # 如果结束位置图元也存在，则做同样操作
        if self.end_item is not None:
            end_pos = self.end_item.pos()
            self.gr_edge.set_dst(end_pos.x()+patch, end_pos.y()+patch)
        else:
            self.gr_edge.set_dst(src_pos.x()+patch, src_pos.y()+patch)
        self.gr_edge.update()

    def remove_from_current_items(self):
        self.end_item = None
        self.start_item = None
	
	# 移除线条
    def remove(self):
        self.remove_from_current_items()
        self.scene.remove_edge(self.gr_edge)
        self.gr_edge = None

 
class GraphicScene(QGraphicsScene):

    def __init__(self, parent=None):
        super().__init__(parent)

        # 一些关于网格背景的设置
        self.grid_size = 20  # 一块网格的大小 （正方形的）
        self.grid_squares = 5  # 网格中正方形的区域个数
		
		# 一些颜色
        self._color_background = QColor('#393939')
        self._color_light = QColor('#2f2f2f')
        self._color_dark = QColor('#292929')
		# 一些画笔
        self._pen_light = QPen(self._color_light)
        self._pen_light.setWidth(1)
        self._pen_dark = QPen(self._color_dark)
        self._pen_dark.setWidth(2)
		
		# 设置画背景的画笔
        self.setBackgroundBrush(self._color_background)
        self.setSceneRect(0, 0, 500, 500)

        self.nodes = []  # 存储图元
        self.edges = []  # 存储连线
    
    def add_node(self, node):
        self.nodes.append(node)
        self.addItem(node)

    def remove_node(self, node):
        self.nodes.remove(node)
        # 删除图元时，遍历与其连接的线，并移除
        for edge in self.edges:
            if edge.edge_wrap.start_item is node or edge.edge_wrap.end_item is node:
                self.remove_edge(edge)
        self.removeItem(node)

    def add_edge(self, edge):
        self.edges.append(edge)
        self.addItem(edge)

    def remove_edge(self, edge):
        self.edges.remove(edge)
        self.removeItem(edge)
	
	# override
    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)
		
		# 获取背景矩形的上下左右的长度，分别向上或向下取整数
        left = int(math.floor(rect.left()))
        right = int(math.ceil(rect.right()))
        top = int(math.floor(rect.top()))
        bottom = int(math.ceil(rect.bottom()))
		
		# 从左边和上边开始
        first_left = left - (left % self.grid_size)  # 减去余数，保证可以被网格大小整除
        first_top = top - (top % self.grid_size)
		
		# 分别收集明、暗线
        lines_light, lines_dark = [], []
        for x in range(first_left, right, self.grid_size):
            if x % (self.grid_size * self.grid_squares) != 0:
                lines_light.append(QLine(x, top, x, bottom))
            else:
                lines_dark.append(QLine(x, top, x, bottom))
		
        for y in range(first_top, bottom, self.grid_size):
            if y % (self.grid_size * self.grid_squares) != 0:
                lines_light.append(QLine(left, y, right, y))
            else:
                lines_dark.append(QLine(left, y, right, y))
		
		# 最后把收集的明、暗线分别画出来
        painter.setPen(self._pen_light)
        if lines_light:
            painter.drawLines(*lines_light)

        painter.setPen(self._pen_dark)
        if lines_dark:
            painter.drawLines(*lines_dark)


class GraphicView(QGraphicsView):

    def __init__(self, graphic_scene, parent=None):
        super().__init__(parent)

        self.gr_scene = graphic_scene  # 将scene传入此处托管，方便在view中维护
        self.parent = parent

        self.init_ui()

        self.edge_enable = False  # 用来记录目前是否可以画线条
        self.drag_edge = None  # 记录拖拽时的线

    def init_ui(self):
        self.setScene(self.gr_scene)
        # 设置渲染属性
        self.setRenderHints(QPainter.Antialiasing |                    # 抗锯齿
                            QPainter.HighQualityAntialiasing |         # 高品质抗锯齿
                            QPainter.TextAntialiasing |                # 文字抗锯齿
                            QPainter.SmoothPixmapTransform |           # 使图元变换更加平滑
                            QPainter.LosslessImageRendering)           # 不失真的图片渲染
        # 视窗更新模式
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        # 设置水平和竖直方向的滚动条不显示
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setTransformationAnchor(self.AnchorUnderMouse)
        # 设置拖拽模式
        self.setDragMode(self.RubberBandDrag)
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_N:
        # 当按下N键时，会在scene的（0,0）位置出现此图元
            print("N")
            item = GraphicItem()
            item.setPos(0, 0)
            # self.gr_scene.addItem(item)
            # self.gr_scene.removeItem(item)
            self.gr_scene.add_node(item)
            # self.gr_scene.remove_item(item)

        # 当按下键盘E键时，启动线条功能，再次按下则是关闭
        if event.key() == Qt.Key_E:
            self.edge_enable = ~self.edge_enable


    def mousePressEvent(self, event):
        item = self.get_item_at_click(event)
        if event.button() == Qt.RightButton:
            if isinstance(item, GraphicItem):
                self.gr_scene.remove_node(item)
        elif self.edge_enable:
            if isinstance(item, GraphicItem):
            	# 确认起点是图元后，开始拖拽
                self.edge_drag_start(item)
        else:
        	# 如果写到最开头，则线条拖拽功能会不起作用
            super().mousePressEvent(event)

    # override
    def mouseReleaseEvent(self, event):
        if self.edge_enable:
        	# 拖拽结束后，关闭此功能
            self.edge_enable = False
            item = self.get_item_at_click(event)
            # 终点图元不能是起点图元，即无环图
            if isinstance(item, GraphicItem) and item is not self.drag_start_item:
                self.edge_drag_end(item)
            else:
                self.drag_edge.remove()
                self.drag_edge = None
        else:
            super().mouseReleaseEvent(event)
	
	# override
    def mouseMoveEvent(self, event):
    	# 实时更新线条
        pos = event.pos()
        if self.edge_enable and self.drag_edge is not None:
            sc_pos = self.mapToScene(pos)
            self.drag_edge.gr_edge.set_dst(sc_pos.x(), sc_pos.y())
            self.drag_edge.gr_edge.update()

    def get_item_at_click(self, event):
        """ 获取点击位置的图元，无则返回None. """
        pos = event.pos()
        item = self.itemAt(pos)
        return item

    def get_items_at_rubber_select(self):
      area = self.rubberBandRect()
      return self.items(area)   # 返回一个所有选中图元的列表，对此操作即可
    
    def edge_drag_start(self, item):
        self.drag_start_item = item  # 拖拽开始时的图元，此属性可以不在__init__中声明
        self.drag_edge = Edge(self.gr_scene, self.drag_start_item, None)

 
    def edge_drag_end(self, item):
        new_edge = Edge(self.gr_scene, self.drag_start_item, item)  # 拖拽结束
        self.drag_edge.remove()  # 删除拖拽时画的线
        self.drag_edge = None
        new_edge.store()  # 保存最终产生的连接线




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.scene = GraphicScene(self)
        self.view = GraphicView(self.scene, self)
        # 有view就要有scene
        self.view.setScene(self.scene)
        # 设置view可以进行鼠标的拖拽选择
        self.view.setDragMode(self.view.RubberBandDrag)

        self.setMinimumHeight(500)
        self.setMinimumWidth(500)
        self.setCentralWidget(self.view)
        self.setWindowTitle("Graphics Demo")

def demo_run():
    app = QApplication(sys.argv)
    demo = MainWindow()
    # 适配 Retina 显示屏（选写）.
    app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    # ----------------------------------
    demo.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    demo_run()






# import sys
# from PyQt5.QtWidgets import *
# from PyQt5.QtCore import *
# from PyQt5.QtWidgets import QMainWindow
# import math

# from PyQt5.QtWidgets import QGraphicsScene
# from PyQt5.QtGui import *
# from PyQt5.QtCore import QLine
# from PyQt5.QtWidgets import QGraphicsItem, QGraphicsPixmapItem
# from PyQt5.QtGui import QPixmap

# class GraphicItem(QGraphicsPixmapItem):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.pix = QPixmap("image.jpg")
#         self.width = 50    # 图元宽
#         self.height = 50   # 图元高
#         self.setPixmap(self.pix)  # 设置图元
#         self.setFlag(QGraphicsItem.ItemIsSelectable)  # ***设置图元是可以被选择的
#         self.setFlag(QGraphicsItem.ItemIsMovable)     # ***设置图元是可以被移动的

# class GraphicEdge(QGraphicsPathItem):
#     def __init__(self, edge_wrap, parent=None):
#         super().__init__(parent)
#         # 这个参数是GraphicEdge的包装类，见下文
#         self.edge_wrap = edge_wrap
#         self.width = 3.0  # 线条的宽度
#         self.pos_src = [0, 0]  # 线条起始位置 x，y坐标
#         self.pos_dst = [0, 0]  # 线条结束位置

#         self._pen = QPen(QColor("#000"))  # 画线条的
#         self._pen.setWidthF(self.width)

#         self._pen_dragging = QPen(QColor("#000"))  # 画拖拽线条时线条的
#         self._pen_dragging.setStyle(Qt.DashDotLine)
#         self._pen_dragging.setWidthF(self.width)

#         self.setFlag(QGraphicsItem.ItemIsSelectable)  # 线条可选
#         self.setZValue(-1)  # 让线条出现在所有图元的最下层

#     def set_src(self, x, y):
#         self.pos_src = [x, y]

#     def set_dst(self, x, y):
#         self.pos_dst = [x, y]
	
# 	# 计算线条的路径
#     def calc_path(self):
#         path = QPainterPath(QPointF(self.pos_src[0], self.pos_src[1]))  # 起点
#         path.lineTo(self.pos_dst[0], self.pos_dst[1])  # 终点
#         return path
	
# 	# override
#     def boundingRect(self):
#         return self.shape().boundingRect()
	
# 	# override
#     def shape(self):
#         return self.calc_path()
	
# 	# override
#     def paint(self, painter, graphics_item, widget=None):
#         self.setPath(self.calc_path()) # 设置路径
#         path = self.path()
#         if self.edge.end_item is None: 
#         	# 包装类中存储了线条开始和结束位置的图元
#         	# 刚开始拖拽线条时，并没有结束位置的图元，所以是None
#         	# 这个线条画的是拖拽路径，点线
#             painter.setPen(self._pen_dragging)
#             painter.drawPath(path)
#         else:
#         	# 这画的才是连接后的线
#             painter.setPen(self._pen)
#             painter.drawPath(path)

# class Edge:
#     def __init__(self, scene, start_item, end_item):
#     	# 参数分别为场景、开始图元、结束图元
#         super().__init__()
#         self.scene = scene
#         self.start_item = start_item
#         self.end_item = end_item
		
# 		# 线条图形在此处创建
#         self.gr_edge = GraphicEdge(self)
#         # 此类一旦被初始化就在添加进scene
#         self.scene.add_edge(self.gr_edge)
		
# 		# 开始更新
#         if self.start_item is not None:
#             self.update_positions()
	
# 	# 最终保存进scene
#     def store(self):
#         self.scene.add_edge(self.gr_edge)
	
# 	# 更新位置
#     def update_positions(self):
#     	# src_pos 记录的是开始图元的位置，此位置为图元的左上角
#         src_pos = self.start_item.pos()
#         # 想让线条从图元的中心位置开始，让他们都加上偏移
#         patch = self.start_item.width / 2
#         self.gr_edge.set_src(src_pos.x()+patch, src_pos.y()+patch)
#         # 如果结束位置图元也存在，则做同样操作
#         if self.end_item is not None:
#             end_pos = self.end_item.pos()
#             self.gr_edge.set_dst(end_pos.x()+patch, end_pos.y()+patch)
#         else:
#             self.gr_edge.set_dst(src_pos.x()+patch, src_pos.y()+patch)
#         self.gr_edge.update()

#     def remove_from_current_items(self):
#         self.end_item = None
#         self.start_item = None
	
# 	# 移除线条
#     def remove(self):
#         self.remove_from_current_items()
#         self.scene.remove_edge(self.gr_edge)
#         self.gr_edge = None


# class GraphicView(QGraphicsView):

#     def __init__(self, graphic_scene, parent=None):
#         super().__init__(parent)

#         self.gr_scene = graphic_scene  # 将scene传入此处托管，方便在view中维护
#         self.parent = parent

#         self.init_ui()

#     def init_ui(self):
#         self.setScene(self.gr_scene)
#         # 设置渲染属性
#         self.setRenderHints(QPainter.Antialiasing |                    # 抗锯齿
#                             QPainter.HighQualityAntialiasing |         # 高品质抗锯齿
#                             QPainter.TextAntialiasing |                # 文字抗锯齿
#                             QPainter.SmoothPixmapTransform |           # 使图元变换更加平滑
#                             QPainter.LosslessImageRendering)           # 不失真的图片渲染
#         # 视窗更新模式
#         self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
#         # 设置水平和竖直方向的滚动条不显示
#         self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
#         self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
#         self.setTransformationAnchor(self.AnchorUnderMouse)
#         # 设置拖拽模式
#         self.setDragMode(self.RubberBandDrag)
    
#     def keyPressEvent(self, event):
#         if event.key() == Qt.Key_N:
#         # 当按下N键时，会在scene的（0,0）位置出现此图元
#             print("N")
#             item = GraphicItem()
#             item.setPos(0, 0)
#             self.gr_scene.addItem(item)
#             # self.gr_scene.removeItem(item)
#             # self.gr_scene.add_node(item)
#             # self.gr_scene.remove_item(item)

#     def mousePressEvent(self, event):
#         super().mousePressEvent(event)
#         if event.button() == Qt.RightButton:   # 判断鼠标右键点击
#             item = self.get_item_at_click(event)
#             if isinstance(item, GraphicItem):  # 判断点击对象是否为图元的实例
#                 self.gr_scene.removeItem(item)

#     def get_item_at_click(self, event):
#         """ 获取点击位置的图元，无则返回None. """
#         pos = event.pos()
#         item = self.itemAt(pos)
#         return item

#     def get_items_at_rubber_select(self):
#       area = self.rubberBandRect()
#       return self.items(area)   # 返回一个所有选中图元的列表，对此操作即可
    
#     def edge_drag_start(self, item):
#         self.drag_start_item = item  # 拖拽开始时的图元，此属性可以不在__init__中声明
#         self.drag_edge = Edge(self.gr_scene, self.drag_start_item, None)

 
#     def edge_drag_end(self, item):
#         new_edge = Edge(self.gr_scene, self.drag_start_item, item)  # 拖拽结束
#         self.drag_edge.remove()  # 删除拖拽时画的线
#         self.drag_edge = None
#         new_edge.store()  # 保存最终产生的连接线

    


 
# class GraphicScene(QGraphicsScene):

#     def __init__(self, parent=None):
#         super().__init__(parent)

#         # 一些关于网格背景的设置
#         self.grid_size = 20  # 一块网格的大小 （正方形的）
#         self.grid_squares = 5  # 网格中正方形的区域个数
		
# 		# 一些颜色
#         self._color_background = QColor('#393939')
#         self._color_light = QColor('#2f2f2f')
#         self._color_dark = QColor('#292929')
# 		# 一些画笔
#         self._pen_light = QPen(self._color_light)
#         self._pen_light.setWidth(1)
#         self._pen_dark = QPen(self._color_dark)
#         self._pen_dark.setWidth(2)
		
# 		# 设置画背景的画笔
#         self.setBackgroundBrush(self._color_background)
#         self.setSceneRect(0, 0, 500, 500)

#         self.nodes = []  # 存储图元
#         self.edges = []  # 存储连线
    
    
#     def add_node(self, node):
#         self.nodes.append(node)
#         self.addItem(node)

#     def remove_node(self, node):
#         self.nodes.remove(node)
#         self.removeItem(node)

#     def add_edge(self, edge):
#         self.edges.append(edge)
#         self.addItem(edge)

#     def remove_edge(self, edge):
#         self.edges.remove(edge)
#         self.removeItem(edge)
	
# 	# override
#     def drawBackground(self, painter, rect):
#         super().drawBackground(painter, rect)
		
# 		# 获取背景矩形的上下左右的长度，分别向上或向下取整数
#         left = int(math.floor(rect.left()))
#         right = int(math.ceil(rect.right()))
#         top = int(math.floor(rect.top()))
#         bottom = int(math.ceil(rect.bottom()))
		
# 		# 从左边和上边开始
#         first_left = left - (left % self.grid_size)  # 减去余数，保证可以被网格大小整除
#         first_top = top - (top % self.grid_size)
		
# 		# 分别收集明、暗线
#         lines_light, lines_dark = [], []
#         for x in range(first_left, right, self.grid_size):
#             if x % (self.grid_size * self.grid_squares) != 0:
#                 lines_light.append(QLine(x, top, x, bottom))
#             else:
#                 lines_dark.append(QLine(x, top, x, bottom))
		
#         for y in range(first_top, bottom, self.grid_size):
#             if y % (self.grid_size * self.grid_squares) != 0:
#                 lines_light.append(QLine(left, y, right, y))
#             else:
#                 lines_dark.append(QLine(left, y, right, y))
		
# 		# 最后把收集的明、暗线分别画出来
#         painter.setPen(self._pen_light)
#         if lines_light:
#             painter.drawLines(*lines_light)

#         painter.setPen(self._pen_dark)
#         if lines_dark:
#             painter.drawLines(*lines_dark)



# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.scene = GraphicScene(self)
#         self.view = GraphicView(self.scene, self)
#         # 有view就要有scene
#         self.view.setScene(self.scene)
#         # 设置view可以进行鼠标的拖拽选择
#         self.view.setDragMode(self.view.RubberBandDrag)

#         self.setMinimumHeight(500)
#         self.setMinimumWidth(500)
#         self.setCentralWidget(self.view)
#         self.setWindowTitle("Graphics Demo")

# def demo_run():
#     app = QApplication(sys.argv)
#     demo = MainWindow()
#     # 适配 Retina 显示屏（选写）.
#     app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
#     app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
#     # ----------------------------------
#     demo.show()
#     sys.exit(app.exec_())

# if __name__ == '__main__':
#     demo_run()


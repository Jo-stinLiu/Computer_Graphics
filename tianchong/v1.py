import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel)
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt


widget_length = 900
widget_width = 600

class Node:
    # 定义节点
    def __init__(self, data):
        self._data = data
        self._next = None

    def get_data(self):
        return self._data

    def get_next(self):
        return self._next

    def set_data(self, ddata):
        self._data = ddata

    def set_next(self, nnext):
        self._next = nnext

class SingleLinkList:
    # 定义链表

    def __init__(self):
        #初始化链表为空
        self._head = None
        self._size = 0

    def get_head(self):
        #获取链表头
        return self._head

    def is_empty(self):
        #判断链表是否为空
        return self._head is None

    def append(self, data):
        #在链表尾部追加一个节点
        temp = Node(data)
        if self._head is None:
            self._head = temp
        else:
            node = self._head
            while node.get_next() is not None:
                node = node.get_next()
            node.set_next(temp)
        self._size += 1

    def remove(self, data):
        # 在链表尾部删除一个节点
        node = self._head
        prev = None
        while node is not None:
            if node.get_data() == data:
                if not prev:
                    # 父节点为None
                    self._head = node.get_next()
                else:
                    prev.set_next(node.get_next())
                break
            else:
                prev = node
                node = node.get_next()
        self._size -= 1


class DemoApp(QMainWindow):

    def __init__(self):
        super(DemoApp, self).__init__()
        self.init_ui()
        self.PList = []
        self.setclear = 0
        self.drawdone = 0


    def init_ui(self):
        self.resize(widget_length, widget_width)
        self.setWindowTitle('多边形填色')
        self.mylabel = QLabel(self)
        self.mylabel.setGeometry(20, 10, 500, 30)
        self.mylabel.setText('通过鼠标点击绘制多边形，点完最后一个点后按下"s"键以连成\n多边形，并自动填充颜色，按下"d"可清空画布')

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:

            if self.drawdone == 1:
                self.drawdone = 0
                self.PList = []
                self.update()

            s = event.pos()
            print('cur:', s.x(), s.y())

            self.PList.append([s.x(), s.y()])

            self.update()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        qp.setPen(Qt.black)

        def PoliFill(polygon):
            l = len(polygon)
            temList = []
            Ymax = 0
            Ymin = widget_width
            (width, height) = (widget_width, widget_length)

            # 求最大最小边
            for [x, y] in enumerate(polygon):
                temList.append(y[1])
                if Ymin > y[1]:
                    Ymin = y[1]
                if Ymax < y[1]:
                    Ymax = y[1]

            print(temList)
            temList = list(set(temList))


            # 初始化并建立NET表
            NET = []
            for i in range(height):
                NET.append(None)


            for i in temList:
                for j in range(0, l):
                    if polygon[j][1] == i:
                        # 左边顶点y是否大于y0
                        if (polygon[(j - 1 + l) % l][1]) > polygon[j][1]:
                            [x1, y1] = polygon[(j - 1 + l) % l]
                            [x0, y0] = polygon[j]
                            delta_x = (x1 - x0) / (y1 - y0)
                            NET[i] = SingleLinkList()
                            NET[i].append([x0, delta_x, y1])

                        # 右边顶点y是否大于y0
                        if (polygon[(j + 1 + l) % l][1]) > polygon[j][1]:
                            [x1, y1] = polygon[(j + 1 + l) % l]
                            [x0, y0] = polygon[j]
                            delta_x = (x1 - x0) / (y1 - y0)
                            if (NET[i] is not None):
                                NET[i].append([x0, delta_x, y1])
                            else:
                                NET[i] = SingleLinkList()
                                NET[i].append([x0, delta_x, y1])

            # 建立活性边表
            AET = SingleLinkList()
            for y in range(Ymin, Ymax + 1):
                # 更新 start_x
                if not AET.is_empty():
                    node = AET.get_head()
                    while True:
                        [start_x, delta_x, ymax] = node.get_data()
                        start_x += delta_x
                        node.set_data([start_x, delta_x, ymax])
                        node = node.get_next()
                        if node is None:
                            break

                # 填充
                if not AET.is_empty():
                    node = AET.get_head()
                    x_list = []
                    # 获取所有交点的x坐标
                    while True:
                        [start_x, _, _] = node.get_data()
                        x_list.append(start_x)
                        node = node.get_next()
                        if node is None:
                            break

                    # 排序
                    x_list.sort()
                    # 两两配对填充
                    for i in range(0, len(x_list), 2):
                        x1 = x_list[i]
                        x2 = x_list[i + 1]
                        # for pixel in range(int(x1), int(x2)+1):
                        #     image[y][pixel] = color
                        qp.drawLine(x1, y, x2, y)

                if not AET.is_empty():
                    # 删除非活性边
                    node = AET.get_head()
                    while True:
                        [start_x, delta_x, ymax] = node.get_data()
                        if ymax == y:
                            AET.remove([start_x, delta_x, ymax])
                        node = node.get_next()
                        if node is None:
                            break

                # 添加活性边
                if NET[y] is not None:
                    node = NET[y].get_head()
                    while True:
                        AET.append(node.get_data())
                        node = node.get_next()
                        if node is None:
                            break


        if self.setclear == 1:
            self.setclear = 0
            self.PList = []
            return

        if len(self.PList) > 1:
            pre = self.PList[0]
            for i in range(1, len(self.PList)):
                cur = self.PList[i]
                qp.drawLine(pre[0], pre[1], cur[0], cur[1])
                pre = cur

        if self.drawdone == 1:
            pre = self.PList[0]
            cur = self.PList[-1]
            qp.drawLine(pre[0], pre[1], cur[0], cur[1])
            PoliFill(self.PList)

    def keyPressEvent(self, event):
        print("按下：" + str(event.key()))
        # print(Qt.Key_D)
        if event.key() == Qt.Key_D:
            # print('yes')
            self.setclear = 1
            self.update()

        if event.key() == Qt.Key_S:
            # print('yes')
            self.drawdone = 1
            self.update()


def run_it():
    app = QApplication(sys.argv)
    w = DemoApp()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run_it()

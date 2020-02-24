import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel)
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt
import math
import numpy as np


widget_length = 1000
widget_width = 700

xshift = 100
yshift = 20
theta = math.pi / 6         #30度角
scalesize = 1.1

class DemoApp(QMainWindow):
    def __init__(self):
        super(DemoApp, self).__init__()
        self.init_ui()
        self.PList = []             #存放多边形的点

        self.setclear = 0           #清空画板
        self.toT = 0                #平移
        self.toR = 0                #旋转
        self.toS = 0                #缩放
        self.drawL = 0              #画线段
        self.drawC = 0              #画圆
        self.drawP = 0              #画多边形

    def init_ui(self):
        self.resize(widget_length, widget_width)
        self.setWindowTitle('2D几何变换')
        self.mylabel = QLabel(self)
        self.mylabel.setGeometry(20, 10, 600, 30)
        self.mylabel.setText('按"L"键绘制线段，按"C"键绘制圆，按"P"键绘制多边形(结束时要再按一次)，按"D"键清空画布\n按"T"键进行平移，按"R"键进行旋转，按"S"键进行缩放')

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:        #添加点到列表，用于记录
            s = event.pos()
            print('cur:', s.x(), s.y())
            self.PList.append([s.x(), s.y()])
            print(self.PList)
        else:
            print('error, mousePress not defined!')
            exit()

        self.update()

    def keyPressEvent(self, event):
        print("按下：" + str(event.key()))
        # print(Qt.Key_D)
        if event.key() == Qt.Key_L:
            self.drawL = 1
            self.PList = []
        elif event.key() == Qt.Key_C:
            self.drawC = 1
            self.PList = []
        elif event.key() == Qt.Key_P:
            if self.drawP == 1:
                print('done!!!!!')
                self.drawP = 2
            else:
                self.drawP = 1
                self.PList = []
        elif event.key() == Qt.Key_D:
            self.setclear = 1
        elif event.key() == Qt.Key_T:
            self.toT = 1
        elif event.key() == Qt.Key_R:
            self.toR = 1
        elif event.key() == Qt.Key_S:
            self.toS = 1
        else:
            print('error, keyPress not defined!')
            # exit()

        self.update()


    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        qp.setPen(Qt.black)

        if self.toT == 1:
            tem = []
            for i in self.PList:
                tem.append([i[0] + xshift, i[1] + yshift])
            self.PList = tem
            self.toT = 0

        if self.toR == 1:
            if self.drawC == 0:
                xlist = []
                ylist = []
                for i in self.PList:
                    xlist.append(i[0])
                    ylist.append(i[1])
                xcenter = np.mean(xlist)
                ycenter = np.mean(ylist)

                sintheta = math.sin(theta)
                costheta = math.cos(theta)

                for i in range(len(self.PList)):
                    xlist[i] = xlist[i] - xcenter
                    ylist[i] = ylist[i] - ycenter

                    xt = xlist[i] * costheta - ylist[i] * sintheta
                    yt = xlist[i] * sintheta + ylist[i] * costheta

                    xt = xt + xcenter
                    yt = yt + ycenter
                    self.PList[i] = [xt, yt]
            self.toR = 0

        if self.toS == 1:
            xlist = []
            ylist = []
            for i in self.PList:
                xlist.append(i[0])
                ylist.append(i[1])
            xcenter = np.mean(xlist)
            ycenter = np.mean(ylist)
            for i in range(len(self.PList)):
                xlist[i] = (xlist[i] - xcenter) * scalesize + xcenter
                ylist[i] = (ylist[i] - ycenter) * scalesize + ycenter

            for i in range(len(self.PList)):
                self.PList[i] = [xlist[i], ylist[i]]

            self.toS = 0



        if self.drawL == 1:
            if len(self.PList) == 2:
                pre = self.PList[0]
                cur = self.PList[1]
                qp.drawLine(pre[0], pre[1], cur[0], cur[1])
                # self.drawL = 0
            else:
                print('error, PList size not correct')
        if self.drawC == 1:
            if len(self.PList) == 2:
                c = self.PList[0]
                t = self.PList[1]
                r = math.sqrt((c[0] - t[0]) * (c[0] - t[0]) + (c[1] - t[1]) * (c[1] - t[1]))
                qp.drawEllipse(c[0]-r, c[1]-r, 2*r, 2*r)
                # self.drawC = 0
            else:
                print('error, PList size not correct')
        if self.drawP == 1 or self.drawP == 2:
            if len(self.PList) > 1:
                pre = self.PList[0]
                for i in range(1, len(self.PList)):
                    cur = self.PList[i]
                    qp.drawLine(pre[0], pre[1], cur[0], cur[1])
                    pre = cur

            if self.drawP == 2:
                pre = self.PList[0]
                cur = self.PList[-1]
                qp.drawLine(pre[0], pre[1], cur[0], cur[1])


        if self.setclear == 1:
            self.setclear = 0  # 清空画板
            self.toT = 0  # 平移
            self.toR = 0  # 旋转
            self.toS = 0  # 缩放
            self.drawL = 0  # 画线段
            self.drawC = 0  # 画圆
            self.drawP = 0  # 画多边形

            self.PList = []
            return


def run_it():
    app = QApplication(sys.argv)
    w = DemoApp()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run_it()
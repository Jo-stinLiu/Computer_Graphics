import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel)
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt
import numpy as np

widget_length = 1000
widget_width = 700

def isIn(startPoint, endPoint, p):
    return (endPoint[0] - startPoint[0]) * (p[1] - startPoint[1]) - (endPoint[1] - startPoint[1]) * (
                p[0] - startPoint[0])

def get_crossing(s1, s2, s3, s4):
    xa, ya = s1[0], s1[1]
    xb, yb = s2[0], s2[1]
    xc, yc = s3[0], s3[1]
    xd, yd = s4[0], s4[1]
    #判断两条直线是否相交，矩阵行列式计算
    a = np.matrix(
        [
            [xb-xa, -(xd-xc)],
            [yb-ya, -(yd-yc)]
        ]
    )
    delta = np.linalg.det(a)
    #不相交,返回两线段
    if np.fabs(delta) < 1e-6:
        print(delta)
        return None
    #求两个参数lambda和miu
    c = np.matrix(
        [
            [xc-xa, -(xd-xc)],
            [yc-ya, -(yd-yc)]
        ]
    )
    d = np.matrix(
        [
            [xb-xa, xc-xa],
            [yb-ya, yc-ya]
        ]
    )
    lamb = np.linalg.det(c)/delta
    miu = np.linalg.det(d)/delta
    #相交
    # if lamb <= 1 and lamb >= 0 and miu >= 0 and miu <= 1:
    #     x = xc + miu*(xd-xc)
    #     y = yc + miu*(yd-yc)
    #     return [x, y]
    # #相交在延长线上
    # else:
    #     return [0, 0]
    # 相交

    x = xc + miu * (xd - xc)
    y = yc + miu * (yd - yc)
    return [x, y]

class DemoApp(QMainWindow):
    def __init__(self):
        super(DemoApp, self).__init__()
        self.init_ui()

        self.PList = []     #存放多边形的点
        self.RList = []     #存放矩形的点
        self.isDone = 0     #用于标记是否绘制完多边形
        self.Start = 0      #开始裁剪

    def init_ui(self):
        self.resize(widget_length, widget_width)
        self.setWindowTitle('裁剪算法')
        self.mylabel = QLabel(self)
        self.mylabel.setGeometry(20, 10, 600, 50)
        self.mylabel.setText('用鼠标选定多边形的点，选取完成后按下"A"键完成绘制多边形。\n随后用鼠标选取正则矩形窗口，选取完成后按下"S"键开始裁剪\n按下"D"键清空画布')

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:        #添加点到列表，用于记录
            s = event.pos()
            print('cur:', s.x(), s.y())
            if self.isDone == 0:
                self.PList.append([s.x(), s.y()])
                print("PList:", self.PList)
            else:
                self.RList.append([s.x(), s.y()])
                print("RList:", self.RList)
        else:
            print('error, mousePress not defined!')
            exit()

        self.update()

    def keyPressEvent(self, event):
        print("按下：" + str(event.key()))
        # print(Qt.Key_D)
        if event.key() == Qt.Key_D:
            self.PList = []
            self.RList = []
            self.isDone = 0
            self.Start = 0
        elif event.key() == Qt.Key_A:
            self.isDone = 1
        elif event.key() == Qt.Key_S:
            self.Start = 1
        else:
            print('error, keyPress not defined!')
            # exit()

        self.update()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        qp.setPen(Qt.black)

        def SutherlandHodgman():
            L = self.RList[0]
            R = self.RList[1]
            rList = [[L[0], L[1]], [R[0], L[1]], [R[0], R[1]], [L[0], R[1]]]
            print("rList:", rList)
            # return

            rPre = rList[-1]

            for i in range(len(rList)):
                temp = []
                rCur = rList[i]

                if len(self.PList) == 0:
                    return
                pre = self.PList[-1]
                flag = 0
                if isIn(rPre, rCur, pre) > 0:           #flag = 1, 表示在内部
                    flag = 1
                for j in range(len(self.PList)):
                    cur = self.PList[j]

                    print("\n", i, j, rPre, rCur, pre, cur, "flag:", flag)

                    if isIn(rPre, rCur, self.PList[j]) <= 0:    #当前点在外侧
                        if flag == 1:                           #前一点在内侧
                            temp.append(get_crossing(rPre, rCur, pre, cur))
                        flag = 0
                    else:                                       #当前点在内侧
                        if flag == 0:                           #前一点在外侧
                            temp.append(get_crossing(rPre, rCur, pre, cur))
                        temp.append(cur)
                        flag = 1

                    print("temp:", temp)
                    pre = cur
                self.PList = temp
                rPre = rCur


        if self.Start == 1:
            SutherlandHodgman()

        if len(self.PList) > 1:
            pre = self.PList[0]
            for i in range(1, len(self.PList)):
                cur = self.PList[i]
                qp.drawLine(pre[0], pre[1], cur[0], cur[1])
                pre = cur
            if self.isDone == 1:
                pre = self.PList[0]
                cur = self.PList[-1]
                qp.drawLine(pre[0], pre[1], cur[0], cur[1])

        if len(self.RList) == 2 and self.Start == 0:
            L = self.RList[0]
            R = self.RList[1]
            qp.drawLine(L[0], L[1], R[0], L[1])
            qp.drawLine(R[0], L[1], R[0], R[1])
            qp.drawLine(R[0], R[1], L[0], R[1])
            qp.drawLine(L[0], R[1], L[0], L[1])

def run_it():
    app = QApplication(sys.argv)
    w = DemoApp()
    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    run_it()
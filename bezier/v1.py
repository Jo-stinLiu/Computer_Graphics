import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel)
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt

widget_length = 900
widget_width = 600

class DemoApp(QMainWindow):
    def __init__(self):
        super(DemoApp, self).__init__()
        self.init_ui()
        self.PList = []         #存储控制点
        self.setclear = 0       #清空标志


    def init_ui(self):
        self.resize(widget_length, widget_width)
        self.setWindowTitle('低次bezier曲线')
        self.mylabel = QLabel(self)
        self.mylabel.setGeometry(20, 10, 500, 30)
        self.mylabel.setText('通过鼠标点击输入控制点，程序将自动根据控制点绘制bezier曲线，按下"d"可清空画布')

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            s = event.pos()
            print('cur:', s.x(), s.y())
            self.PList.append([s.x(), s.y()])
            self.update()

    def keyPressEvent(self, event):
        print("按下：" + str(event.key()))
        # print(Qt.Key_D)
        if event.key() == Qt.Key_D:
            # print('yes')
            self.setclear = 1
            self.update()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        qp.setPen(Qt.black)

        if self.setclear == 1:
            self.setclear = 0
            self.PList = []

        if len(self.PList) == 2:
            pre = self.PList[0]
            cur = self.PList[1]
            qp.drawLine(pre[0], pre[1], cur[0], cur[1])
        elif len(self.PList) == 3:
            P0 = self.PList[0]
            P1 = self.PList[1]
            P2 = self.PList[2]
            pre = P0
            for i in range(0, 10001, 1):
                t = i / 10000
                a0 = (1 - t) ** 2
                a1 = 2 * t * (1-t)
                a2 = t ** 2
                x = a0 * P0[0] + a1 * P1[0] + a2 * P2[0]
                y = a0 * P0[1] + a1 * P1[1] + a2 * P2[1]
                qp.drawLine(pre[0], pre[1], x, y)
                pre = [x, y]
        elif len(self.PList) == 4:
            [P0, P1, P2, P3] = self.PList
            pre = P0
            for i in range(0, 10001, 1):
                t = i / 10000
                a0 = (1 - t) ** 3
                a1 = 3 * t * (1-t) ** 2
                a2 = 3 * t ** 2 * (1 - t)
                a3 = t ** 3
                x = a0 * P0[0] + a1 * P1[0] + a2 * P2[0] + a3 * P3[0]
                y = a0 * P0[1] + a1 * P1[1] + a2 * P2[1] + a3 * P3[1]
                qp.drawLine(pre[0], pre[1], x, y)
                pre = [x, y]
        elif len(self.PList) == 5:
            [P0, P1, P2, P3, P4] = self.PList
            pre = P0
            for i in range(0, 10001, 1):
                t = i / 10000
                a0 = (1 - t) ** 4
                a1 = 4 * t * (1 - t) ** 3
                a2 = 6 * t ** 2 * (1 - t) ** 2
                a3 = 4 * t ** 3 * (1 - t)
                a4 = t ** 4
                x = a0 * P0[0] + a1 * P1[0] + a2 * P2[0] + a3 * P3[0] + a4 * P4[0]
                y = a0 * P0[1] + a1 * P1[1] + a2 * P2[1] + a3 * P3[1] + a4 * P4[1]
                qp.drawLine(pre[0], pre[1], x, y)
                pre = [x, y]


def run_it():
    app = QApplication(sys.argv)
    w = DemoApp()
    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    run_it()

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
        self.setWindowTitle('均匀3次B样条曲线')
        self.mylabel = QLabel(self)
        self.mylabel.setGeometry(20, 10, 500, 30)
        self.mylabel.setText('通过鼠标点击输入控制点，当控制点达到要求后开始绘制，\n随后，每增加控制点，曲线跟随绘制，按下"d"可清空画布')

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

        if len(self.PList) > 3:
            for i in range(0, len(self.PList) - 3):
                [P0, P1, P2, P3] = self.PList[i:i+4]
                # print([P0, P1, P2, P3])
                pre = -1
                for i in range(0, 5001, 1):
                    t = i / 5000
                    a0 = 1 / 6 * (1 - t) ** 3
                    a1 = 1 / 6 * (3 * t ** 3 - 6 * t ** 2 + 4)
                    a2 = 1 / 6 * (-3 * t ** 3 + 3 * t ** 2 + 3 * t + 1)
                    a3 = 1 / 6 * t ** 3
                    x = a0 * P0[0] + a1 * P1[0] + a2 * P2[0] + a3 * P3[0]
                    y = a0 * P0[1] + a1 * P1[1] + a2 * P2[1] + a3 * P3[1]
                    if (pre != -1):
                        qp.drawLine(pre[0], pre[1], x, y)
                    pre = [x, y]

def run_it():
    app = QApplication(sys.argv)
    w = DemoApp()
    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    run_it()

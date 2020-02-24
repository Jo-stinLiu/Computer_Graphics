# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel)
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt
import math

class AppDemo(QMainWindow):

    def __init__(self):
        super(AppDemo, self).__init__()
        self.init_ui()
        self.x = self.y = 0.0
        self.cur_x = self.cur_y = 0.0

    def init_ui(self):
        self.resize(900, 600)
        self.setWindowTitle('鼠标拖拽画圆')

        self.label_mouse_x = QLabel(self)
        self.label_mouse_x.setGeometry(800, 5, 80, 30)
        self.label_mouse_x.setText('x')
        self.label_mouse_x.setMouseTracking(True)

        self.label_mouse_y = QLabel(self)
        self.label_mouse_y.setText('y')
        self.label_mouse_y.setGeometry(800, 40, 80, 30)
        self.label_mouse_y.setMouseTracking(True)

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            s = event.pos()
            print(s.x(), s.y())
            self.x = s.x()
            self.y = s.y()


    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        qp.setPen(Qt.black)

        l = []
        x0 = self.x
        y0 = self.y
        r = math.sqrt((self.cur_x - x0) * (self.cur_x - x0) + (self.cur_y - y0) * (self.cur_y - y0))
        # r = 100
        x = 0
        y = r
        d = 1.25 - r
        print('    ', x0, y0, r)
        while x <= y:
            if d >= 0:
                x = x + 0.005
                y = y - 0.005
                d = d + 2 * (x - y) + 5
            else:
                x = x + 0.005
                d = d + 2 * x + 3
            pos_tmp = (x, y)
            l.append(pos_tmp)

        if len(l) > 1:
            point_start = l[0]
            for pos_tmp in l:
                point_end = pos_tmp
                qp.drawLine(x0 + point_start[0], y0 + point_start[1], x0 + point_end[0], y0 + point_end[1])
                point_start = point_end

            point_start = l[0]
            for pos_tmp in l:
                point_end = pos_tmp
                qp.drawLine(x0 + point_start[0], y0 - point_start[1], x0 + point_end[0], y0 - point_end[1])
                point_start = point_end

            point_start = l[0]
            for pos_tmp in l:
                point_end = pos_tmp
                qp.drawLine(x0 - point_start[0], y0 + point_start[1], x0 - point_end[0], y0 + point_end[1])
                point_start = point_end

            point_start = l[0]
            for pos_tmp in l:
                point_end = pos_tmp
                qp.drawLine(x0 - point_start[0], y0 - point_start[1], x0 - point_end[0], y0 - point_end[1])
                point_start = point_end

            point_start = l[0]
            for pos_tmp in l:
                point_end = pos_tmp
                qp.drawLine(x0 + point_start[1], y0 + point_start[0], x0 + point_end[1], y0 + point_end[0])
                point_start = point_end

            point_start = l[0]
            for pos_tmp in l:
                point_end = pos_tmp
                qp.drawLine(x0 + point_start[1], y0 - point_start[0], x0 + point_end[1], y0 - point_end[0])
                point_start = point_end

            point_start = l[0]
            for pos_tmp in l:
                point_end = pos_tmp
                qp.drawLine(x0 - point_start[1], y0 + point_start[0], x0 - point_end[1], y0 + point_end[0])
                point_start = point_end

            point_start = l[0]
            for pos_tmp in l:
                point_end = pos_tmp
                qp.drawLine(x0 - point_start[1], y0 - point_start[0], x0 - point_end[1], y0 - point_end[0])
                point_start = point_end

        qp.end()


    def mouseMoveEvent(self, event):
        s = event.pos()
        self.setMouseTracking(True)
        self.cur_x = s.x()
        self.cur_y = s.y()
        self.label_mouse_x.setText('X:' + str(s.x()))
        self.label_mouse_y.setText('Y:' + str(s.y()))
        print(self.cur_x, self.cur_y)

        self.update()



def run_it():
    app = QApplication(sys.argv)
    w = AppDemo()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run_it()
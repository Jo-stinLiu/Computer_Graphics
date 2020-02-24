import sys
from PyQt5.QtWidgets import (QApplication, QWidget)
from PyQt5.QtGui import (QPainter, QPen)
from PyQt5.QtCore import Qt

class Example(QWidget):

    def __init__(self):
        super(Example, self).__init__()

        #resize设置宽高，move设置位置
        self.resize(400, 300)
        self.move(100, 100)
        self.setWindowTitle("简单的画板1.0")

        #setMouseTracking设置为False，否则不按下鼠标时也会跟踪鼠标事件
        self.setMouseTracking(False)

        #设置两个变量接收移动中的点的x、y坐标
        self.pos_x = 20
        self.pos_y = 20

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        painter.setPen(pen)

        #定点(20, 20) 到 (self.pos_x, self.pos_y)之间画线
        painter.drawLine(20, 20, self.pos_x, self.pos_y)

        painter.end()

    def mouseMoveEvent(self, event):
        '''
            按住鼠标移动事件：更新pos_x和pos_y的值
            调用update()函数在这里相当于调用paintEvent()函数
            每次update()时，之前调用的paintEvent()留下的痕迹都会清空
        '''
        self.pos_x = event.pos().x()
        self.pos_y = event.pos().y()

        self.update()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pyqt_learn = Example()
    pyqt_learn.show()
    app.exec_()
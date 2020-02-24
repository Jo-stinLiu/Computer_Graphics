import matplotlib.pyplot as plt

class point:
    def __init__(self):
        self.x = 0
        self.y = 0

a = point()
b = point()
a.x, a.y, b.x, b.y = map(int, input().split())      #输入两点坐标

# print(a.x, a.y, b.x, b.y)

x = a.x                 #画线起点
y = a.y
dx = abs(b.x - a.x)         #计算dx与dy
dy = abs(b.y - a.y)

Precision = 0.02        #设置精度，或者说步长

s1 = 0
if b.x > a.x:           #表示从左往右画
    s1 = Precision
else:                   #表示从右往左画
    s1 = -Precision

s2 = 0
if b.y > a.y:           #表示从下往上画
    s2 = Precision
else:                   #表示从上往下画
    s2 = -Precision

interchange = 0         #指明是否交换过
if dy > dx:             #y轴变化大的话，交换x轴与y轴
    temp = dx
    dx = dy
    dy = temp
    interchange = 1
else:
    interchange = 0

p = 2 * dy - dx
# print(dx)
X = []
Y = []
i = 0
while i <= dx:
    # plt.plot(x, y)
    X.append(x)
    Y.append(y)
    if p >= 0:
        if interchange == 0:
            y = y + s2
        else:
            x = x + s1
        p = p - 2 * dx
    if interchange == 0:
        x = x + s1
    else:
        y = y + s2
    p = p + 2 * dy
    i += Precision
# print(1)
plt.plot(X, Y)
plt.show()
print('success')
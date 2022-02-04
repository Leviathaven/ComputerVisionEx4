import cv2
import numpy as np
from matplotlib import pyplot as plt

height = 8

A = cv2.imread("photos4/pic1.png")
B = cv2.imread("photos4/pic2.png")

# пирамида Гаусса для A
G = A.copy()
gpA = [G]
for i in range(height):
    G = cv2.pyrDown(G)
    gpA.append(G)

# пирамида Гаусса для B
G = B.copy()
gpB = [G]
for i in range(height):
    G = cv2.pyrDown(G)
    gpB.append(G)

# пирамида Лапласа для A
lpA = [gpA[height - 1]]
for i in range(height - 1, 0, -1):
    GE = cv2.pyrUp(gpA[i])
    rows, cols, _ = gpA[i - 1].shape
    GE = GE[:rows, :cols]
    L = cv2.subtract(gpA[i - 1], GE)
    lpA.append(L)

# пирамида Лапласа для B
lpB = [gpB[height - 1]]
for i in range(height - 1, 0, -1):
    GE = cv2.pyrUp(gpB[i])
    rows, cols, _ = gpB[i - 1].shape
    GE = GE[:rows, :cols]
    L = cv2.subtract(gpB[i - 1], GE)
    lpB.append(L)

# соединяем левые и правые части на каждом уровне пирамид
LS = []
for la, lb in zip(lpA, lpB):
    _, cols, _ = la.shape
    ls = np.hstack((la[:, :int(cols / 2)], lb[:, int(cols / 2):]))
    LS.append(ls)

ls_ = LS[0]
for i in range(1, height):
    ls_ = cv2.pyrUp(ls_)
    rows, cols, _ = LS[i].shape
    ls_ = ls_[:rows, :cols]
    ls_ = cv2.add(ls_, LS[i])

# объединение двух половин без блендинга
real = np.hstack((A[:, :int(cols / 2)], B[:, int(cols / 2):]))

cv2.imwrite('photos4/pyramid_blending_' + str(height) + '.jpg', ls_)
cv2.imwrite('photos4/direct_blending.jpg', real)
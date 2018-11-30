# -*- coding: utf-8 -*-
"""

"""

import cv2
import numpy as np

def sift(filename):
    img = cv2.imread(filename)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray,2,3,0.04)

    #result is dilated for marking the corners, not important
    dst = cv2.dilate(dst,None)

    # Threshold for an optimal value, it may vary depending on the image.
    img[dst>0.03*dst.max()]=[0,0,255]
    numbers = len(img[dst>0.03*dst.max()])
    #print(numbers)
    cv2.imwrite("./detectDst/test.jpg", img)
    return numbers
#cv2.imshow('dst',img)

if __name__ == '__main__':
    sift('./5.jpg')
import cv2
import numpy as np
str = "./data/5.jpg"
img = cv2.imread(str)
#img = img[1000:1300,2700:3000]
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
gray = np.float32(gray)
dst = cv2.cornerHarris(gray,2,3,0.04)
dst = cv2.dilate(dst,None)
img[dst>0.05*dst.max()]=[0,0,255]
cv2.imwrite("./data/test5.jpg", img)
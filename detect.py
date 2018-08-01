# -*- coding: utf-8 -*-
"""

"""

import cv2
import numpy as np

def detect_function():
    filename = '5.jpg'
    img = cv2.imread(filename)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    col = len(gray[0])
    row = len(gray)
    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray,2,3,0.04)
    #result is dilated for marking the corners, not important
    arr = dst>0.03*dst.max()
    arr1 = np.zeros((len(arr), len(arr[0])))
    for i in range(len(arr)):
        for j in range(len(arr[0])):
            if arr[i][j] == True:
                arr1[i][j] = 1
            else:
                arr1[i][j] = 0
    index = np.argwhere(arr==1)
    '''
    L = len(index)
    for i in range(L):
        for j in range(i, L):
            if ((index[i][0]==index[j][0])&((index[j][1]-index[i][0])<=10)):
                cv2.line(img,(index[i][1], index[i][0]), (index[i][1], index[i][0]), (0, 0, 255), 3)
            if ((index[i][1]==index[j][1])&((index[j][0]-index[i][0])<=3)):
                cv2.line(img,(index[i][1], index[i][0]), (index[j][1], index[i][0]), (0, 0, 255), 3)
    cv2.imwrite("rect5.jpg", img)
    '''

    '''
    length = 10
    height = 6
    MAX_DIST = np.sqrt(length**2+height**2)
    start_length = int(length/2)
    start_height = int(height/2)
    pair = []
    L = len(index)
    for i in range(start_height, row, height):
        for j in range(start_length, col, height):
            pair.append([i, j])
    NUM = len(pair)
    rect = []
    count = 0
    for k in range(NUM):
        for r in range(L):
            if np.linalg.norm(pair[k]-index[r])<MAX_DIST-1:
                    count += 1
        #print(k,count)
        if count >=6:
            rect.append(pair[k])
        count = 0
    M = len(rect)
    for i in range(M):
        cv2.rectangle(img, (rect[i][1]-start_length, rect[i][0]-start_height), (rect[i][1]+start_length, rect[i][0]+start_height), (0, 0, 255), 1)
    
    #cv2.rectangle(img, (1, 242), (393, 245), (0, 0, 255), 1)
    cv2.imwrite("rect5.jpg", img)
    #cv2.imshow('dst',img)
    '''
    count = 0
    for i in range(1, row, 2):
        for j in range(4, col, 4):
            count = sum(arr[i-1, j-4:j+4])+sum(arr[i, j-4:j+4])+sum(arr[i+1, j-4:j+4])
            if count>=4:
                cv2.rectangle(img, (j-4 , i-1), (j+4, i+1), (0, 0, 255), 1)
    cv2.imwrite("rect5.jpg", img)

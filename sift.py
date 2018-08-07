# -*- coding: utf-8 -*-
"""

"""

import cv2
import numpy as np

def sift():
    filename = '5.jpg'
    img = cv2.imread(filename)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray,2,3,0.04)

    #result is dilated for marking the corners, not important
    dst = cv2.dilate(dst,None)

    # Threshold for an optimal value, it may vary depending on the image.
    img[dst>0.03*dst.max()]=[0,0,255]
    cv2.imwrite("test5.jpg", img)
#cv2.imshow('dst',img)

'''
def process_image(imagename, resultname, params="--edge-thresh 10 --peak-thresh 5"):
    """ 处理一幅图像，然后将结果保存在文件中"""

    if imagename[-3:] != 'pgm':
        #创建一个pgm文件
        im = Image.open(imagename).convert('L')
        im.save('tmp.pgm')
        imagename ='tmp.pgm'
    cmmd = str("sift "+imagename+" --output="+resultname+" "+params)
    os.system(cmmd)
    print 'processed', imagename, 'to', resultname

def read_features_from_file(filename):
    """读取特征属性值，然后将其以矩阵的形式返回"""
    f = loadtxt(filename)
    return f[:,:4], f[:,4:] #特征位置，描述子
'''
# if cv2.waitKey(0) & 0xff == 27:
#     cv2.destroyAllWindows()
'''
def write_featrues_to_file(filename, locs, desc):
    """将特征位置和描述子保存到文件中"""
    savetxt(filename, hstack((locs,desc)))

def plot_features(im, locs, circle=False):
    """显示带有特征的图像
       输入：im（数组图像），locs（每个特征的行、列、尺度和朝向）"""

    def draw_circle(c,r):
        t = arange(0,1.01,.01)*2*pi
        x = r*cos(t) + c[0]
        y = r*sin(t) + c[1]
        plot(x, y, 'b', linewidth=2)

    imshow(im)
    if circle:
        for p in locs:
            draw_circle(p[:2], p[2])
    else: 
        plot(locs[:,0], locs[:,1], 'ob')
    axis('off')

imname = 'empire.jpg'
im1 = array(Image.open(imname).convert('L'))
process_image(imname, 'empire.sift')
l1,d1 = read_features_from_file('empire.sift')

figure()
gray()
plot_features(im1, l1, circle=True)
show()
'''
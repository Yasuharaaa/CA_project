# -*- coding: utf-8 -*-

import cv2
import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog
from MainWin import Ui_MainWindow
from PyQt5 import QtGui
from detect import *
from sift import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5.QtGui import *
import qdarkstyle
from PyQt5 import QtWidgets
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
#import matplotlib.pyplot as plt
from getFileName import *
from cropImg import *
import time
import pygame
import csv
import pandas as pd
from inquireFromCsv import *
from readCSV import *
from ZoomWindow import *
import re
from isRoll import *

class MainForm(QMainWindow, Ui_MainWindow, QWidget):
    def __init__(self):
        super(MainForm, self).__init__()
        self.setupUi(self)
        self.model = QStandardItemModel(50, 3)
        self.model.setHorizontalHeaderLabels(['ID', 'Time', 'Status'])

        for row in range(50):
            for column in range(3):
                item = QStandardItem("row %s, column %s" % (row, column))
                self.model.setItem(row, column, item)

        #self.tableView = QTableView()
        self.tableView.setModel(self.model)
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableView.doubleClicked.connect(self.table_change) # 双击事件函数
        dlgLayout = QVBoxLayout()
        dlgLayout.addWidget(self.tableView)
        self.setLayout(dlgLayout)

        self._create_csv()

        #初始化定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showImg)

        # 点击show按钮开始每隔30秒钟显示一次图像
        self.pushButton_2.clicked.connect(self.startTimer)

        # 点击stop按钮暂停图片显示
        self.pushButton_3.clicked.connect(self.endTimer)
        # 点击zoom按钮显示放大的图像
        self.zoom_in.clicked.connect(self.zoomImg)

        # 点击inquire按钮显示需要检测的结果
        self.pushButton.clicked.connect(self.inquire)

        # 点击“回看查询”回看图片
        # self.pushButton_4.clicked.connect(self.playBack)

        # 点击“按时间查询”回看时间轴
        self.pushButton_5.clicked.connect(self.timeTable)

        # 近期疑似毛刺点查询
        self.negButton.clicked.connect(self.negSample)

        #设置字体格式
        self.label_2.setStyleSheet("border:2px solid black;")
        self.label_2.setFont(QFont("Roman times", 20, QFont.Bold))
        self.label_2.setAlignment(Qt.AlignCenter)
        self.label_3.setStyleSheet("border:2px solid black;")
        self.label_3.setFont(QFont("Roman times", 20, QFont.Bold))
        self.label_3.setAlignment(Qt.AlignCenter)
        self.label_4.setStyleSheet("border:2px solid black;")
        self.label_4.setFont(QFont("Roman times", 15, QFont.Bold))
        self.label_4.setAlignment(Qt.AlignCenter)
        self.label_5.setStyleSheet("border:2px solid black;")
        self.label_5.setFont(QFont("Roman times", 15, QFont.Bold))
        self.label_5.setAlignment(Qt.AlignCenter)
        self.label_7.setStyleSheet("border:2px solid black;")
        self.label_10.setStyleSheet("border:2px solid red;")
        self.label_12.setStyleSheet("border:2px solid blue;")
        self.pushButton.setFont(QFont("Roman times", 10, QFont.Bold))
        self.pushButton_2.setFont(QFont("Roman times", 15, QFont.Bold))
        self.zoom_in.setFont(QFont("Roman times", 15, QFont.Bold))
        self.pushButton_3.setFont(QFont("Roman times", 15, QFont.Bold))
        self.pushButton_5.setFont(QFont("Roman times", 10, QFont.Bold))

        self.storeDest1 = 'C:/ca_project/Demo/front'  # 正面图片初始保存位置
        self.storeDest2 = 'C:/ca_project/Demo/back'  # 背面图片初始保存位置
        self.finalDest1 = 'C:/ca_project/Demo/frontfinal'
        self.finalDest2 = 'C:/ca_project/Demo/backfinal'
        self.cropedDst1 = "C:/ca_project/Demo/cropedImageFwd/image_croped.jpg"
        self.cropedDst2 = "C:/ca_project/Demo/cropedImageBwd/image_croped.jpg"
        self.numbers = 0 #检测到角点个数
        self.findNew1 = False #目标路径下是否有新的图片
        self.findNew2 = False
        self.numbers1 = 0
        self.number2 = 0
        pygame.init()

    def closeEvent(self, event): # 退出警告
        ret = QMessageBox.question(self, "警告", "确定要退出吗?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if ret == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def negSample(self):
        pass

    def table_change(self, index): # index为当前点击的行列好
        QMessageBox.about(self, "双击事件", "双击事件触发成功: " + str(self.model.data(self.model.index(index.row(), 0))))

    def startTimer(self): #启动定时器
        self.timer.start(5000)
        self.pushButton_2.setEnabled(False)
        self.pushButton_3.setEnabled(True)

    def endTimer(self): # 结束定时器
        self.timer.stop()
        pygame.mixer.music.stop()
        self.pushButton_2.setEnabled(True)
        self.pushButton_3.setEnabled(False)

    # def playBack(self): #回看图片
    #     playBackID = self.lineEdit_2.text()
    #     self.s3 = PlayBackWindow()
    #     self.s3.setWindowTitle('回看图片')
    #     playDst = self.finalDest1 + '/' + playBackID + '.jpg'
    #     if os.path.exists(playDst):
    #         self.s3.label_10.setPixmap(QtGui.QPixmap(playDst))
    #         self.s3.label_10.setScaledContents(True)  # 让图片自适应label大小
    #         # self.setStyleSheet("background: black")
    #         self.s3.label_10.setStyleSheet("border:2px solid black;")
    #         if not self.s3.isVisible():
    #             self.s3.show()
    #     else:
    #         reply = QMessageBox.about(self, "查询结果", "未找到符合要求的钢卷，请重新输入")

    def zoomImg(self):  #放大图片
        self.s1 = SecondWindow()
        self.s1.setWindowTitle('Fwd')
        self.s1.label_10.setPixmap(QtGui.QPixmap("./detectDst/test1.jpg"))
        self.s1.label_10.setScaledContents(True)  # 让图片自适应label大小
        # self.setStyleSheet("background: black")
        self.s1.label_10.setStyleSheet("border:2px solid black;")
        if not self.s1.isVisible():
            self.s1.show()

        self.s2 = SecondWindow()
        self.s2.setWindowTitle('Bwd')
        self.s2.label_10.setPixmap(QtGui.QPixmap("./detectDst/test2.jpg"))
        self.s2.label_10.setScaledContents(True)  # 让图片自适应label大小
        # self.setStyleSheet("background: black")
        self.s2.label_10.setStyleSheet("border:2px solid black;")
        if not self.s2.isVisible():
            self.s2.show()


    def inquire(self):  #查询数据
        kwd = self.lineEdit.text() #获得输入钢卷ID
        # print(str)
        #self.textBrowser.setText(str)
        df = pd.read_csv('./database/database.csv')
        #print(df)
        # find, s1, s2, s3 = getCSV(kwd)
        self.play_back = PictureZoom()
        #self.paly_back.setWindowTitle("回放")
        self.play_back.show()
        #print(find)
        # if (find == False):
        #      reply = QMessageBox.about(self, "查询结果", "未找到符合要求的钢卷，请重新输入")
        # else:
        #      reply = QMessageBox.about(self, "查询结果", "ID: " + s1 + "\tTime: " + s2 + "\tStatus: " + s3)

        #print(reply)


    def _selfCheck(self, src): # 检查文件夹中是否有没拍到钢卷的图像，有的话删除
        file_name_list = os.listdir(src)
        # print(file_name_list)
        check(src, file_name_list)




    def showImg(self):  #显示图片
        self._selfCheck(self.storeDest1) # 除错图
        self._selfCheck(self.storeDest2)
        if not os.listdir(self.storeDest1) or not os.listdir(self.storeDest2): # 没有图则不做任何操作
            return
        findNew1, imgName1 = new_report(self.storeDest1, self.finalDest1)
        findNew2, imgName2 = new_report(self.storeDest2, self.finalDest2)
        #print(findNew1, imgName1, findNew2, imgName2)

        pygame.mixer.music.stop()

        self.cropName1 = cropAndSave(imgName1, self.cropedDst1)
        #print(self.cropName1)
        self.label_2.setPixmap(QtGui.QPixmap(imgName1))
        self.label_2.setScaledContents(True)  # 让图片自适应label大小
        self.numbers1 = sift(self.cropName1, 1)
        if self.numbers1 > 500:
            self.label_2.setStyleSheet("border:2px solid red;")
            #print(self.numbers1)
        else:
            self.label_2.setStyleSheet("border:2px solid black;")

        self.cropName2 = cropAndSave(imgName2, self.cropedDst2)
        self.label_3.setPixmap(QtGui.QPixmap(imgName2))
        self.label_3.setScaledContents(True)  # 让图片自适应label大小
        self.numbers2 = sift(self.cropName2, 2)
        if self.numbers2 > 500:
            self.label_3.setStyleSheet("border:2px solid red;")
        else:
            self.label_3.setStyleSheet("border:2px solid black;")

        #print(self.numbers1)
        #print(self.numbers2)
        if self.numbers1 > 200 or self.numbers2 > 200:
            #print(2)
            track = pygame.mixer.music.load(r"./sound/1.mp3")
            pygame.mixer.music.play()

        else:
            #print(1)
            pygame.mixer.music.stop()
            pygame.init()
        #print(self.numbers1, self.numbers2)

        num, df = readCSV('./database/database.csv')
        self.updateTable(num, df)


        str = "当前正面图像为" + imgName1 + "\n" + "当前反面图像为" + imgName2
        self.textBrowser.setText(str)
        self.textBrowser.setFont(QFont("Microsoft YaHei", 15))

    def updateTable(self, num, df):
        #pass
        if (num>50):
            for row in range(50):
                item = QStandardItem(str(df[-row-1][0]))
                self.model.setItem(row, 0, item)
                item = QStandardItem(df[-row-1][1])
                self.model.setItem(row, 1, item)
                item = QStandardItem(df[-row-1][2])
                self.model.setItem(row, 2, item)

        else:
            for row in range(num):
                item = QStandardItem(str(df[-row-1][0]))
                self.model.setItem(row, 0, item)
                item = QStandardItem(str(df[-row-1][1]))
                self.model.setItem(row, 1, item)
                item = QStandardItem(str(df[-row-1][2]))
                self.model.setItem(row, 2, item)
                item.setBackground(QColor(255, 0, 0))

    def timeTable(self):
        text = self.lineEdit_3.text()
        # print(text)
        if (not re.match('^[0-9]+-[0-9]+', text)):
            QMessageBox.about(self, "错误", "时间查询有误，请检查并重新输入")
        else:
            self.s4 = TimeWindow()
            self.s4.setWindowTitle('回看数据')
            if not self.s4.isVisible():
                self.s4.show()

    def _create_csv(self):
        if (not os.path.exists('./database/database.csv')):
            with open('./database/database.csv', 'w+') as f:
                csv_write = csv.writer(f)
                csv_head = ["ID", "Time", "Status"]
                csv_write.writerow(csv_head)

    def createDB(self): #连接至数据库
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('c:/ca_project/Demo/TestSql/database.db')

        if not db.open():
            QMessageBox.critical(None, ("无法打开数据库"),
                                 ("无法建立到数据库的连接,这个例子需要SQLite 支持，请检查数据库配置。\n\n"
                                  "点击取消按钮退出应用。"),
                                 QMessageBox.Cancel)
            return False


class SecondWindow(QWidget):
    def __init__(self, parent=None):
        super(SecondWindow, self).__init__(parent)
        self.resize(1010, 1010)
        self.label_10 = QtWidgets.QLabel(self)
        self.label_10.setGeometry(QtCore.QRect(5, 5, 1000, 1000))
        self.label_10.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label_10.setLineWidth(10)
        self.label_10.setObjectName("label_10")

class PlayBackWindow(QWidget):
    def __init__(self, parent=None):
        super(PlayBackWindow, self).__init__(parent)
        self.resize(1900, 910)
        self.table1 = QTableView()
        self.table1.setGeometry(QtCore.QRect(5, 5, 1800, 900))
        self.table1.setLineWidth(10)
        self.scene1 = QGraphicsScene(self)
        self.item1 = QGraphicsPixmapItem()
        #item1.setPixmap(QPixmap('./Miane.jpg'))
        # scene1 = QGraphicsScene()
        # scene1.addItem(item1)
        # self.table1.setModel(scene1)
        # self.label_10 = QtWidgets.QLabel(self)
        # self.label_10.setGeometry(QtCore.QRect(5, 5, 900, 900))
        # self.label_10.setFrameShadow(QtWidgets.QFrame.Plain)
        # self.label_10.setLineWidth(10)
        # self.label_10.setObjectName("label_10")
        #
        # self.label_11 = QtWidgets.QLabel(self)
        # self.label_11.setGeometry(QtCore.QRect(5, 910, 900, 900))
        # self.label_11.setFrameShadow(QtWidgets.QFrame.Plain)
        # self.label_11.setLineWidth(10)
        # self.label_11.setObjectName("label_11")



class PictureZoom(QMainWindow, Zoom_Window):
    """
    Class documentation goes here.
    """

    def __init__(self, parent=None, file_name = 'Miane.jpg'):
        """
        Constructor

        @param parent reference to the parent widget
        @type QWidget
        """
        super(PictureZoom, self).__init__(parent)
        self.setupUi(self)
        img = cv2.imread(file_name)  # 读取图像
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 转换图像通道
        x = img.shape[1]  # 获取图像大小
        y = img.shape[0]
        self.zoomscale = 1  # 图片放缩尺度
        frame = QImage(img, x, y, QImage.Format_RGB888)
        pix = QPixmap.fromImage(frame)
        self.item = QGraphicsPixmapItem(pix)  # 创建像素图元
        # self.item.setScale(self.zoomscale)
        self.scene = QGraphicsScene()  # 创建场景
        self.scene.addItem(self.item)
        self.picshow.setScene(self.scene)  # 将场景添加至视图
        self.setWindowTitle("回放")

    @pyqtSlot()
    def on_zoomin_clicked(self):
        """
        点击缩小图像
        """
        # TODO: not implemented yet
        self.zoomscale = self.zoomscale - 0.05
        if self.zoomscale <= 0:
            self.zoomscale = 0.2
        self.item.setScale(self.zoomscale)  # 缩小图像

    @pyqtSlot()
    def on_zoomout_clicked(self):
        """
        点击方法图像
        """
        # TODO: not implemented yet
        self.zoomscale = self.zoomscale + 0.05
        if self.zoomscale >= 1.2:
            self.zoomscale = 1.2
        self.item.setScale(self.zoomscale)  # 放大图像



class TimeWindow(QWidget):
    def __init__(self, parent=None):
        super(TimeWindow, self).__init__(parent)
        self.resize(400, 1800)
        self.tableView = QtWidgets.QTableView()
        self.tableView.setGeometry(QtCore.QRect(10, 10, 380, 1800))
        self.tableView.setObjectName("tableView")
        self.model = QStandardItemModel(50, 3)
        self.model.setHorizontalHeaderLabels(['ID', 'Time', 'Status'])
        self.zoomWin = PictureZoom()

        for row in range(50):
            for column in range(3):
                item = QStandardItem("row %s, column %s" % (row, column))
                self.model.setItem(row, column, item)

        # self.tableView = QTableView()
        self.tableView.setModel(self.model)
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        dlgLayout = QVBoxLayout()
        dlgLayout.addWidget(self.tableView)
        self.setLayout(dlgLayout)
        self.tableView.doubleClicked.connect(self.showZoomImg)

    def showZoomImg(self, index):
        #
        #QMessageBox.about(self, "双击事件", "双击事件触发成功: " + str(self.model.data(self.model.index(index.row(), 0))))

        self.zoomWin.show()













if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    win = MainForm()
    #s = SecondWindow()
    #win.zoom_in.clicked.connect(s.handle_click)
    #win.btn.clicked.connect(ex.hide)
    win.show()
    sys.exit(app.exec_())

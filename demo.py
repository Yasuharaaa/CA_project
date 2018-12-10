# -*- coding: utf-8 -*-

#import cv2
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

class MainForm(QMainWindow, Ui_MainWindow, QWidget):
    def __init__(self):
        super(MainForm, self).__init__()
        self.setupUi(self)
        self.model = QStandardItemModel(10, 3)
        self.model.setHorizontalHeaderLabels(['Item1', 'Item2', 'Item3'])

        for row in range(24):
            for column in range(3):
                item = QStandardItem("row %s, column %s" % (row, column))
                self.model.setItem(row, column, item)

        #self.tableView = QTableView()
        self.tableView.setModel(self.model)
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
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
        self.pushButton.setFont(QFont("Roman times", 15, QFont.Bold))
        self.pushButton_2.setFont(QFont("Roman times", 15, QFont.Bold))
        self.zoom_in.setFont(QFont("Roman times", 15, QFont.Bold))
        self.pushButton_3.setFont(QFont("Roman times", 15, QFont.Bold))

        self.storeDest1 = 'C:/ca_project/Demo/front' #正面图片初始保存位置
        self.storeDest2 = 'C:/ca_project/Demo/back' #背面图片初始保存位置
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

    def startTimer(self): #启动定时器
        self.timer.start(3000)
        self.pushButton_2.setEnabled(False)
        self.pushButton_3.setEnabled(True)

    def endTimer(self): # 结束定时器
        self.timer.stop()
        pygame.mixer.music.stop()
        self.pushButton_2.setEnabled(True)
        self.pushButton_3.setEnabled(False)

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
        print(str)
        #self.textBrowser.setText(str)
        df = pd.read_csv('./database/database.csv')
        #print(df)
        find, s1, s2, s3 = getCSV(kwd)
        #print(find)
        if (find == False):
             reply = QMessageBox.about(self, "查询结果", "未找到符合要求的钢卷，请重新输入")
        else:
             reply = QMessageBox.about(self, "查询结果", "ID: " + s1 + "\tTime: " + s2 + "\tStatus: " + s3)
        #print(reply)

    def showImg(self):  #显示图片
        self.findNew1, imgName1 = new_report(self.storeDest1, self.finalDest1)
        self.findNew2, imgName2 = new_report(self.storeDest2, self.finalDest2)
        #print(self.findNew1, imgName1, self.findNew2, imgName2)
        if self.findNew1:
            self.cropName1 = cropAndSave(imgName1, self.cropedDst1)
            self.label_2.setPixmap(QtGui.QPixmap(imgName1))
            self.label_2.setScaledContents(True)  # 让图片自适应label大小
            self.numbers1 = sift(self.cropName1, 1)
        if self.findNew2:
            self.cropName2 = cropAndSave(imgName2, self.cropedDst2)
            self.label_3.setPixmap(QtGui.QPixmap(imgName2))
            self.label_3.setScaledContents(True)  # 让图片自适应label大小
            self.numbers2 = sift(self.cropName2, 2)

        #print(self.numbers1, self.numbers2)

        pygame.mixer.music.stop()
        if self.numbers1 > 500:
            self.label_2.setStyleSheet("border:2px solid red;")
            if self.numbers2 > 500:
                self.label_3.setStyleSheet("border:2px solid red;")
            #print("播放音乐1")


            #time.sleep(3)
        else:
            self.label_2.setStyleSheet("border:2px solid black;")
            self.label_3.setStyleSheet("border:2px solid black;")

        if self.numbers1 > 500 or self.numbers2 > 500:
            track = pygame.mixer.music.load(r"./sound/1.mp3")

            pygame.mixer.music.play()
        str = "当前正面图像为" + imgName1 + "\n" + "当前反面图像为" + imgName2
        self.textBrowser.setText(str)


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








if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    win = MainForm()
    #s = SecondWindow()
    #win.zoom_in.clicked.connect(s.handle_click)
    #win.btn.clicked.connect(ex.hide)
    win.show()
    sys.exit(app.exec_())

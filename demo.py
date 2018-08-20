# -*- coding: utf-8 -*-

import cv2
import sys
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
import matplotlib.pyplot as plt


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
        # 下面代码让表格100填满窗口
        # self.tableView.horizontalHeader().setStretchLastSection(True)
        # self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        dlgLayout = QVBoxLayout()
        dlgLayout.addWidget(self.tableView)
        self.setLayout(dlgLayout)
        # 点击show按钮显示原始图像
        self.pushButton_2.clicked.connect(self.showImg)
        self.zoom_in.clicked.connect(self.zoomImg)
        # 点击detect按钮显示检测后的图像
        #self.pushButton_2.clicked.connect(self.detect)
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
        # pe = QPalette()
        # #pe.setColor(QPalette.WindowText, Qt.red)  # 设置字体颜色
        # self.label_7.setAutoFillBackground(True)  # 设置背景充满，为设置背景颜色的必要条件
        # self.label_10.setAutoFillBackground(True)
        # self.label_12.setAutoFillBackground(True)
        # pe.setColor(QPalette.Window, Qt.red)  # 设置背景颜色
        # # pe.setColor(QPalette.Background,Qt.blue)<span style="font-family: Arial, Helvetica, sans-serif;">#设置背景颜色，和上面一行的效果一样
        # self.label_7.setPalette(pe)
        # pe.setColor(QPalette.Window, Qt.red)  # 设置背景颜色
        # self.label_10.setPalette(pe)
        # pe.setColor(QPalette.Window, Qt.blue)  # 设置背景颜色
        # self.label_12.setPalette(pe)

    def zoomImg(self):  #放大图片
        self.s = SecondWindow()
        if not self.s.isVisible():
            self.s.show()
    def showImg(self):
        cv2.imread("./5.jpg")
        self.label_2.setPixmap(QtGui.QPixmap("./5.jpg"))
        self.label_2.setScaledContents(True)  # 让图片自适应label大小
        #self.label_2.setScaleContents(True)
        #detect_function()
        sift()
        self.label_3.setPixmap(QtGui.QPixmap("./test5.jpg"))
        self.label_3.setScaledContents(True)  # 让图片自适应label大小
        # self.graphicsView.scene = QtWidgets.QGraphicsScene()
        # item = QtWidgets.QGraphicsPixmapItem("./5.jpg")
        # self.graphicsView.scene.addItem(item)
        # self.graphicsView.setScene(self.graphicsView.scene)
        self.label_2.setStyleSheet("border:2px solid red;")
        self.label_3.setStyleSheet("border:2px solid red;")

    def createDB(self): #创建数据库
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
        self.resize(1500, 1500)
        self.label_10 = QtWidgets.QLabel(self)
        self.label_10.setGeometry(QtCore.QRect(150, 150, 1000, 1000))
        self.label_10.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label_10.setLineWidth(10)
        self.label_10.setObjectName("label_10")
        self.label_10.setPixmap(QtGui.QPixmap("./test5.jpg"))
        self.label_10.setScaledContents(True)  # 让图片自适应label大小
        # self.setStyleSheet("background: black")
        self.label_10.setStyleSheet("border:2px solid red;")





if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    win = MainForm()
    #s = SecondWindow()
    #win.zoom_in.clicked.connect(s.handle_click)
    #win.btn.clicked.connect(ex.hide)
    win.show()
    sys.exit(app.exec_())

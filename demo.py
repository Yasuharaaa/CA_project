# -*- coding: utf-8 -*-

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

class MainForm(QMainWindow, Ui_MainWindow, QWidget):
    def __init__(self):
        super(MainForm, self).__init__()
        self.setupUi(self)
        self.model = QStandardItemModel(10, 3);
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


    def showImg(self):
        self.label_2.setPixmap(QtGui.QPixmap("./5.jpg"))
        #self.label_2.setScaleContents(True)
        #detect_function()
        sift()
        self.label_3.setPixmap(QtGui.QPixmap("./test5.jpg"))
        # self.graphicsView.scene = QtWidgets.QGraphicsScene()
        # item = QtWidgets.QGraphicsPixmapItem("./5.jpg")
        # self.graphicsView.scene.addItem(item)
        # self.graphicsView.setScene(self.graphicsView.scene)
        self.label_2.setStyleSheet("border:2px solid red;")
        self.label_3.setStyleSheet("border:2px solid red;")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    win = MainForm()
    win.show()
    sys.exit(app.exec_())

# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog
from MainWin import Ui_MainWindow
from PyQt5 import QtGui
from detect import *


class MainForm(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainForm, self).__init__()
        self.setupUi(self)
        # 点击show按钮显示原始图像
        self.pushButton.clicked.connect(self.showImg)

        # 点击detect按钮显示检测后的图像
        self.pushButton_2.clicked.connect(self.detect)

    def showImg(self):
        self.label_2.setPixmap(QtGui.QPixmap("./5.jpg"))
        #self.label_2.setScaleContents(True)
    def detect(self):
        detect_function()
        self.label_3.setPixmap(QtGui.QPixmap("./rect5.jpg"))



if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainForm()
    win.show()
    sys.exit(app.exec_())

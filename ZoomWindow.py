from PyQt5 import QtCore, QtGui, QtWidgets

"""
放大界面UI配置
"""
class Zoom_Window(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Replay")
        MainWindow.resize(800, 600)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.picshow = QtWidgets.QGraphicsView(self.centralWidget)
        self.picshow.setObjectName("picshow")
        self.gridLayout.addWidget(self.picshow, 0, 1, 3, 1)
        self.zoomout = QtWidgets.QPushButton(self.centralWidget)
        self.zoomout.setObjectName("zoomout")
        self.gridLayout.addWidget(self.zoomout, 0, 0, 1, 1)
        self.zoomin = QtWidgets.QPushButton(self.centralWidget)
        self.zoomin.setObjectName("zoomin")
        self.gridLayout.addWidget(self.zoomin, 1, 0, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.zoomout.setText(_translate("MainWindow", "放大"))
        self.zoomin.setText(_translate("MainWindow", "缩小"))

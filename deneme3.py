# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'denem1.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from __future__ import annotations
from PyQt5 import QtCore, QtGui, QtWidgets

from typing import *
import sys
import os
from matplotlib.backends.qt_compat import QtCore, QtWidgets
# from PyQt5 import QtWidgets, QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvas
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import random
#import xlsxwriter

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 601)
        #---
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("logo.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        MainWindow.setWindowIcon(icon)
        #---
        #self.setWindowIcon(QtGui.QIcon('logo.png'))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 2, 1, 1, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setObjectName("pushButton_6")
        self.gridLayout_2.addWidget(self.pushButton_6, 0, 1, 1, 1)
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setObjectName("pushButton_5")
        self.gridLayout_2.addWidget(self.pushButton_5, 0, 0, 1, 1)
        self.pushButton_7 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_7.setObjectName("pushButton_7")
        self.gridLayout_2.addWidget(self.pushButton_7, 1, 0, 1, 1)
        self.pushButton_8 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_8.setObjectName("pushButton_8")
        self.gridLayout_2.addWidget(self.pushButton_8, 1, 1, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 3, 1, 1, 1)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.comboBox = QtWidgets.QComboBox(self.tab)
        self.comboBox.setObjectName("comboBox")
        self.gridLayout_4.addWidget(self.comboBox, 0, 0, 1, 1)
        self.frame = QtWidgets.QFrame(self.tab)
        self.frame.setMinimumSize(QtCore.QSize(594, 471))
        self.frame.setMaximumSize(QtCore.QSize(1600, 900))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        """
        ----------------
        """
        
        self.comboBox.addItems(["All Sensors",data_func_list[0][1],data_func_list[1][1],data_func_list[2][1],data_func_list[3][1]])
        self.comboBox.currentIndexChanged.connect(self.selectionChange)
        
        """
        ----------------
        """
        
        
        """
        ----------------
        """
        self.lyt = QtWidgets.QGridLayout()
        self.frame.setLayout(self.lyt)
        
        self.myFig1 = MyFigureCanvas(100,data_list["temperature"] , interval=1,index = 0)
        self.lyt.addWidget(self.myFig1,1,1)
        
        self.myFig2 = MyFigureCanvas(100,data_list["pressure"] , interval=1, index = 1)
        self.lyt.addWidget(self.myFig2,1,2)
        
        
        
        self.myFig3 = MyFigureCanvas(100,data_list["altitude"] , interval=1,index = 2)
        self.lyt.addWidget(self.myFig3,2,1)
        
        self.myFig4 = MyFigureCanvas(100,data_list["otherdata"], interval=1,index = 3)
        self.lyt.addWidget(self.myFig4,2,2)
        
        
        
        
        """
        ----------------
        """
        
        
        self.gridLayout_4.addWidget(self.frame, 1, 0, 1, 1)
        
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.graphicsView_2 = QtWidgets.QGraphicsView(self.tab_2)
        self.graphicsView_2.setGeometry(QtCore.QRect(-5, 1, 621, 521))
        self.graphicsView_2.setObjectName("graphicsView_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.gridLayout_3.addWidget(self.tabWidget, 0, 0, 4, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout.addWidget(self.pushButton_3, 3, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 0, 0, 1, 1)
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout.addWidget(self.pushButton_4, 3, 1, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 0, 1, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def selectionChange(self,index):
        
        if index ==0:
            self.ClearLayout(self.lyt)
            self.myFig1 = MyFigureCanvas(100,data_list["temperature"] ,interval=1,index = 0)
            self.lyt.addWidget(self.myFig1,1,1)
            
            self.myFig2 = MyFigureCanvas(100, data_list["pressure"] , interval=1, index = 1)
            self.lyt.addWidget(self.myFig2,1,2)
            
            
            
            self.myFig3 = MyFigureCanvas(100, data_list["altitude"] , interval=1,index = 2)
            self.lyt.addWidget(self.myFig3,2,1)
            
            self.myFig4 = MyFigureCanvas(100, data_list["otherdata"] , interval=1,index = 3)
            self.lyt.addWidget(self.myFig4,2,2)
        
            
        elif index ==1:
            self.ClearLayout(self.lyt)
            self.myFig2 = MyFigureCanvas(100, data_list["temperature"] , interval=1, index = 0)
            self.lyt.addWidget(self.myFig2)
            
            
        elif index ==2:
            self.ClearLayout(self.lyt)
            self.myFig3 = MyFigureCanvas(100, data_list["pressure"] , interval=1,index = 1)
            self.lyt.addWidget(self.myFig3)
            
        elif index ==3:
            self.ClearLayout(self.lyt)
            self.myFig4 = MyFigureCanvas(100, data_list["altitude"] , interval=1,index = 2)
            self.lyt.addWidget(self.myFig4)
        elif index ==4:
            self.ClearLayout(self.lyt)
            self.myFig4 = MyFigureCanvas(100, data_list["otherdata"] , interval=1,index = 3)
            self.lyt.addWidget(self.myFig4)
        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "OZU Rover SSC"))
        self.label_2.setText(_translate("MainWindow", "Shovel Control"))
        self.pushButton_6.setText(_translate("MainWindow", "Shovel Take"))
        self.pushButton_5.setText(_translate("MainWindow", "Shovel Up"))
        self.pushButton_7.setText(_translate("MainWindow", "Shovel Down"))
        self.pushButton_8.setText(_translate("MainWindow", "Shovel Put"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Graphics"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Others"))
        self.pushButton_3.setText(_translate("MainWindow", "Tube 3"))
        self.pushButton.setText(_translate("MainWindow", "Tube 1"))
        self.pushButton_4.setText(_translate("MainWindow", "Tube 4"))
        self.pushButton_2.setText(_translate("MainWindow", "Tube 2"))
        self.label.setText(_translate("MainWindow", "Tube Control"))
    def ClearLayout(self,layout):
        for i in reversed(range(layout.count())): 
            layout.itemAt(i).widget().setParent(None)


class MyFigureCanvas(FigureCanvas):
    '''
    This is the FigureCanvas in which the live plot is drawn.

    '''
    def __init__(self, x_len, data_list ,interval , index):
        '''
        :param x_len:       The nr of data points shown in one plot.
        :param y_range:     Range on y-axis.
        :param interval:    Get a new datapoint every .. milliseconds.

        '''
        super().__init__(mpl.figure.Figure())
        
        # chose the data
        self.index = index
        # Range settings
        self._x_len_ = x_len
        
        self.data_list = data_list
        

        # Store two lists _x_ and _y_
        self._x_ = list(range(0, x_len))
        self._y_ = data_list

        # Store a figure ax
        #plt.subplots(constrained_layout=True)
        self._ax_ = self.figure.subplots()
        #self._ax_.set_ylim(ymin=self._y_range_[0], ymax=self._y_range_[1]) # added
        #----
        self._ax_.set_title(str(data_func_list[self.index][1]))
        
        #----
        lenY = len(self._y_)
        self._y_ = self._y_[lenY-100:lenY] 
        
        self._ax_.set_ylim(ymin=min(self._y_)-min(self._y_)*10//100, ymax=max(self._y_)+max(self._y_)*10//100)
        self._line_ , = self._ax_.plot(self._x_, self._y_)    # added
        #self._ax_.autoscale()
        self.draw()                                                        # added

        # Initiate the timer
        self._timer_ = self.new_timer(interval, [(self._update_canvas_, (), {})])
        self._timer_.start()
        return

    def _update_canvas_(self) -> None:
        '''
        This function gets called regularly by the timer.

        '''
        self._y_.append(round(data_func_list[self.index][0](), 2))     # Add new datapoint
        lenY = len(self._y_)
        self._y_ = self._y_[lenY-100:lenY]                 # Truncate list y
        self._ax_.set_ylim(ymin=min(self._y_)-min(self._y_)*10//100, ymax=max(self._y_)+max(self._y_)*10//100)

        # Previous code
        # --------------
        # self._ax_.clear()                                   # Clear ax
        # self._ax_.plot(self._x_, self._y_)                  # Plot y(x)
        # self._ax_.set_ylim(ymin=self._y_range_[0], ymax=self._y_range_[1])
        # self.draw()

        # New code
        # ---------
        self._line_.set_ydata(self._y_)
        
        self._ax_.draw_artist(self._ax_.patch)
        self._ax_.draw_artist(self._line_)
        
        self.update()
        self.flush_events()
        return

# Data source
# ------------
data_list = {"temperature":[0]*100,"pressure":[0]*100,"altitude":[0]*100,"otherdata":[0]*100}
def temperature():
    """
    f = open("data.txt")
    x = f.readlines()[-1]
    data_listesi = x.split(",")
    k = int(data_listesi[0])
    """
    k = random.randint(20, 30)
    data_list["temperature"].append(k)
    return k

def pressure():
    """
    f = open("data.txt")
    x = f.readlines()[-1]
    data_listesi = x.split(",")
    k = int(data_listesi[1])
    """
    k = random.randint(100, 200)
    data_list["pressure"].append(k)
    return k

def altitude():
    """
    f = open("data.txt")
    x = f.readlines()[-1]
    data_listesi = x.split(",")
    k = int(data_listesi[2])
    """
    k = random.randint(700, 800)
    data_list["altitude"].append(k)
    return k

def otherdata():
    """
    f = open("data.txt")
    x = f.readlines()[-1]
    data_listesi = x.split(",")
    k = int(data_listesi[3])
    """
    k = random.randint(90,100)
    data_list["otherdata"].append(k)
    return k
data_func_list = [(temperature,"temperature"),(pressure,"pressure"),(altitude,"altitude"),(otherdata,"otherdata")]


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())




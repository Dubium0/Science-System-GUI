# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 23:32:39 2022

@author: LENOPC
"""

import sys
import matplotlib as mpl
mpl.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.ticker as ticker
import queue
import numpy as np
import time
import xlsxwriter as xls
import pandas as pd
from PyQt5 import QtCore,QtWidgets,QtGui
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot

import random
"""
temp index  = 0
pressure index  = 1
altitude index  = 2
carbon index  = 3



"""
WINDOW_SIZE = 0

class MyFigureCanvas(FigureCanvas):
    '''
    This is the FigureCanvas in which the live plot is drawn.
    '''
    def __init__(self, x_len ,interval,datas,sensor_name,dataRangeMin,dataRangeMax):
        '''
        :param x_len:       The nr of data points shown in one plot.
        :param y_range:     Range on y-axis.
        :param interval:    Get a new datapoint every .. milliseconds.
        '''
        super().__init__(mpl.figure.Figure())
        # canvas settings
        
        # initialize things
        self.datas = datas
        self.sensor_name = sensor_name
       
        # set range of the datas that will seen
        self._x_len_ = x_len
        
        # Store two lists _x_ and _y_
        self._x_ = list(range(0, x_len))
        
        try:
            self._y_ =  datas[sensor_name][-self._x_len_:] 
        except:
            self._y_ =datas[sensor_name]

        # Store a figure ax
        self.figure.patch.set_facecolor('#3a3a3a')
        
        self._ax_ = self.figure.subplots()
        
        self._ax_.set_facecolor(color ='#3a3a3a')
        self._ax_.spines["top"].set_visible(False)
        self._ax_.spines["right"].set_visible(False)
        self._ax_.spines["left"].set_color('white')
        self._ax_.spines["bottom"].set_color('white')
        self._ax_.tick_params(colors = "white")
        
        # title
        self._ax_.set_title(sensor_name,color = "white")
        
        # set limits of y axes
        self._ax_.set_ylim(ymin=dataRangeMin, ymax=dataRangeMax)
        
        # plot 
        self._line_ , = self._ax_.plot(self._x_, self._y_,marker = ".",color = "white")    
        
        self.draw()                                                        

        # Initiate the timer
        self._timer_ = self.new_timer(interval, [(self._update_canvas_, (), {})])
        self._timer_.start()
    

    def _update_canvas_(self):
        '''
        This function gets called regularly by the timer.
        '''
        #show max xlen data
        
        self._y_ = self.datas[self.sensor_name][-self._x_len_:]     
        
        
        # update things
        
        self._line_.set_ydata(self._y_)
        self._ax_.yaxis.grid(True,linestyle='--')
        self._ax_.draw_artist(self._ax_.patch)
        self._ax_.draw_artist(self._line_)
        
        self.update()
        self.flush_events()
        
        
            
        
        

        
        
class SSGUI(QtWidgets.QMainWindow):
    def __init__(self):
        # initializiton ---------------------------------------------------------------------------
        QtWidgets.QMainWindow.__init__(self)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        self.ui = uic.loadUi("NewDesign.ui",self)
        
        # multi thread
        self.threadpool = QtCore.QThreadPool()
        
        self.setWindowIcon(QtGui.QIcon('logo.png'))
        
        self.setWindowTitle("SSGUI")
        
        #------------------------------------------------------------------------------------------
        
        #---add-logo-------------------------------------------------------------------------------
        
        pixmap  = QtGui.QPixmap("logo.png")
        self.upperSideLabel.setPixmap(pixmap)
        self.upperSideLabel.setScaledContents(True)
        
        #------------------------------------------------------------------------------------------
        
        
        #graph canvas ----------------------------------------------------------------------------
        """
            Initializing graphs 
        
        """
        self.graphGridLayout.addWidget(MyFigureCanvas(100,10,data_dict,"Temperature",10,40),1,1)
        self.graphGridLayout.addWidget(MyFigureCanvas(100,10,data_dict,"Pressure",150,350),1,2)
        self.graphGridLayout.addWidget(MyFigureCanvas(100,10,data_dict,"Altitude",2980,3110),2,1)
        self.graphGridLayout.addWidget(MyFigureCanvas(100,10,data_dict,"Carbon",230,330),2,2)
        #-----------------------------------------------------------------------------------------
        
        #----- combo box-----------------------------------------------------------------------
        
        self.graphComboBox.addItem("All Sensors")
        L = [i for i in data_dict]
        self.graphComboBox.addItems(L)
        
        self.graphComboBox.currentIndexChanged.connect(self.selectionChange)
        
        #-------------------------------------------------------------------------------------------
        
        #---tab icons-------------------------------------------------------------------------------
        
        self.tabWidget.setTabIcon(0,QtGui.QIcon(u"whiteIcons/pie-chart.svg"))
        self.tabWidget.setTabIcon(1,QtGui.QIcon(u"whiteIcons/sliders.svg"))
        self.tabWidget.setTabIcon(2,QtGui.QIcon(u"whiteIcons/aperture.svg"))
        self.tabWidget.setTabIcon(3,QtGui.QIcon(u"whiteIcons/box.svg"))
        
        
        #-------------------------------------------------------------------------------------------
        
        #-----size-grip------------------------------------------------------------------------------
        QtWidgets.QSizeGrip(self.size_grip)
        #--------------------------------------------------------------------------------------------
        
        
        
        #button links ---------------------------------------------------------------------------
        self.startStreamButton.clicked.connect(self.Start_Worker)
        self.startStreamButton.setIcon(QtGui.QIcon(u"whiteIcons/rss.svg"))
        self.createExcelPushButton.clicked.connect(self.Create_Excel_File)
        self.createExcelPushButton.setIcon(QtGui.QIcon(u"whiteIcons/save.svg"))
        #----- essensial buttons -----------
        self.minimizeButton.clicked.connect(lambda: self.showMinimized())
        self.minimizeButton.setIcon(QtGui.QIcon(u"whiteIcons/chevron-down.svg"))
        self.fullSizeButton.clicked.connect(lambda: self.restore_or_maximize_window())
        self.fullSizeButton.setIcon(QtGui.QIcon(u"whiteIcons/maximize.svg"))
        self.exitButton.clicked.connect(lambda: self.close())
        self.exitButton.setIcon(QtGui.QIcon(u"whiteIcons/x.svg"))
        #-------------------------------------------
        #----------------------------------------------------------------------------------------
        
        #---------move window----------------------------------------------------------------------
        def moveWindow(e):
            # Detect if the window is  normal size
            # ###############################################  
            if self.isMaximized() == False: #Not maximized
                # Move window only when window is normal size  
                # ###############################################
                #if left mouse button is clicked (Only accept left mouse button clicks)
                if e.buttons() == QtCore.Qt.LeftButton:  
                    #Move window 
                    self.move(self.pos() + e.globalPos() - self.clickPosition)
                    self.clickPosition = e.globalPos()
                    e.accept()
        self.ui.mouseMoveEvent = moveWindow
        #---------------------------------------------------------------------------------------
        
    
    
    def mousePressEvent(self,event):
         self.clickPosition = event.globalPos()
        
       
    
    def Start_Worker(self):
        worker  = Worker(self.Start_Stream,)
        self.threadpool.start(worker)
    def Start_Stream(self):
        #rospy.init_node("dataIN")
        #rospy.Subscriber("SENSORS",String,callback)
        #rospy.spin()
       
        # test :=)
        while True:
            randomFill()
            time.sleep(0.1)
        
    def Create_Excel_File(self):
        excel = Excel_Creator(data_dict,"science_data_sheet")
        excel.create_excel()
    
        
    def selectionChange(self,index):
        
        if index ==0:
            self.ClearLayout(self.graphGridLayout)
            self.myFig1 = MyFigureCanvas(100,10,data_dict,"Temperature",10,40)
            self.graphGridLayout.addWidget(self.myFig1,1,1)
            
            self.myFig2 =MyFigureCanvas(100,10,data_dict,"Pressure",150,350)
            self.graphGridLayout.addWidget(self.myFig2,1,2)
            
            
            
            self.myFig3 = MyFigureCanvas(100,10,data_dict,"Altitude",2980,3110)
            self.graphGridLayout.addWidget(self.myFig3,2,1)
            
            self.myFig4 = MyFigureCanvas(100,10,data_dict,"Carbon",230,330)
            self.graphGridLayout.addWidget(self.myFig4,2,2)
        
            
        elif index ==1:
            self.ClearLayout(self.graphGridLayout)
            self.myFig2 =MyFigureCanvas(100,10,data_dict,"Temperature",10,40)
            self.graphGridLayout.addWidget(self.myFig2)
            
            
        elif index ==2:
            self.ClearLayout(self.graphGridLayout)
            self.myFig3 = MyFigureCanvas(100,10,data_dict,"Pressure",150,350)
            self.graphGridLayout.addWidget(self.myFig3)
            
        elif index ==3:
            self.ClearLayout(self.graphGridLayout)
            self.myFig4 = MyFigureCanvas(100,10,data_dict,"Altitude",2980,3110)
            self.graphGridLayout.addWidget(self.myFig4)
        elif index ==4:
            self.ClearLayout(self.graphGridLayout)
            self.myFig4 = MyFigureCanvas(100,10,data_dict,"Carbon",230,330)
            self.graphGridLayout.addWidget(self.myFig4)
            
    def ClearLayout(self,layout):
        for i in reversed(range(layout.count())): 
            layout.itemAt(i).widget().setParent(None)
        
    
        
    
    def restore_or_maximize_window(self):
        # Global windows state
        global WINDOW_SIZE  #The default value is zero to show that the size is not maximized
    
        win_status = WINDOW_SIZE

        if win_status == 0:
        	# If the window is not maximized
        	WINDOW_SIZE = 1 #Update value to show that the window has been maxmized
        	self.showMaximized()

        	# Update button icon  when window is maximized
        	self.ui.fullSizeButton.setIcon(QtGui.QIcon(u"whiteIcons/minimize.svg"))#Show minized icon
        else:
        	# If the window is on its default size
            WINDOW_SIZE = 0 #Update value to show that the window has been minimized/set to normal size (which is 800 by 400)
            self.showNormal()

            # Update button icon when window is minimized
            self.ui.fullSizeButton.setIcon(QtGui.QIcon(u"whiteIcons/maximize.svg"))#Show maximize icon

    
    
class Excel_Creator():
    
    def __init__(self,data,file_name):
        self.data = data
        self.df = pd.DataFrame(data)
        self.path = f"./{file_name}.xlsx"
        
        
    def create_excel(self):
        self.df["index"] = list(range(0,len(self.df)))
        # create new excel file
        workbook = xls.Workbook(self.path)
        
        #create sheet1
        worksheet_  = workbook.add_worksheet()
        for index,name in enumerate(self.df.columns):
            worksheet_.write(0,index,name)# 
            worksheet_.write_column(1,index,self.df[name])
            
        col_name = ["A","B","C","D","E","F","G"]
        loc = ["I1","I16","Q1","Q16","Y1","Y16"]
        for index,i in enumerate(self.df.columns):
            # create a blank chart
            chart = workbook.add_chart({"type":"scatter","subtype":"straight"})
            #fill chart categories x-axis  values y-axis
            chart.add_series({"categories":"=Sheet1!${}$2:{}F${}".format(col_name[len(self.df.columns)-1],col_name[len(self.df.columns)-1],len(self.df)+1),
                              "values":"=Sheet1!${}$2:${}${}".format(col_name[index],col_name[index],len(self.df+1)),
                              "name":f"{i}"})
            # name axs
            chart.set_x_axis({'name': 'Index'})
            #chart.set_y_axis({'name': 'Temperature(C)'})
            # add chart to sheet1 at certain position it generally takes 15x8 (lenxwidth) places
            worksheet_.insert_chart(loc[index],chart)
    
    
        workbook.close()
    
    



class Worker(QtCore.QRunnable):

	def __init__(self, function, *args, **kwargs):
		super(Worker, self).__init__()
		self.function = function
		self.args = args
		self.kwargs = kwargs

	@pyqtSlot()
	def run(self):

		self.function(*self.args, **self.kwargs)

           


    

# Data source
# -------------------------------------------------------------------------------------------------------------
data_dict = {"Temperature":[1]*100,"Pressure":[1]*100,"Altitude":[1]*100,"Carbon":[1]*100}


def Sensor_Call_Back(sensor_datas):
    data_list = sensor_datas.data.split(",")
    data_dict["Temperature"].append(float(data_list[0]))
    data_dict["Pressure"].append(float(data_list[1]))
    data_dict["Altitude"].append(float(data_list[2]))
    data_dict["Carbon"].append(float(data_list[3]))
    
    
def randomFill():
    data_dict["Temperature"].append(float(random.randint(20,30)))
    data_dict["Pressure"].append(float(random.randint(200,300)))
    data_dict["Altitude"].append(float(random.randint(3000,3100)))
    data_dict["Carbon"].append(float(random.randint(250,300)))
    
#-----------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(open("Combinear.qss","r").read())
    
    mainWindow = SSGUI()
    mainWindow.show()
    sys.exit(app.exec_())
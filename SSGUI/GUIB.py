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

import time

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
        
        #-important--Variables--------------------------------------------------------------------------------------------
        
        """
            This variables are important for buttons
        
        """

        self.currentPositionTube = 0
        self.destinationTube = 0
        self.isShovelContainerDown = False
        self.isSoilTakenByOuterShovel = False
        self.isSoilTakenByInnerShovel = False
        self.testPosition = 0
        self.currentStatus = ""
        self.pressedAutoFunction = False;
        
        #-----------------------------------------------------------------------------------------------------------------
        
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
        self.graphGridLayout.addWidget(MyFigureCanvas(100,10,data_dict,"Altitude",2980,3110),1,3)
        self.graphGridLayout.addWidget(MyFigureCanvas(100,10,data_dict,"Carbon",230,330),2,1)
        self.graphGridLayout.addWidget(MyFigureCanvas(100,10,data_dict,"Carbon1",230,330),2,2)
        self.graphGridLayout.addWidget(MyFigureCanvas(100,10,data_dict,"Carbon2",230,330),2,3)
        self.graphGridLayout.addWidget(MyFigureCanvas(100,10,data_dict,"Carbon3",230,330),3,1)
        self.graphGridLayout.addWidget(MyFigureCanvas(100,10,data_dict,"Carbon4",230,330),3,2)
        self.graphGridLayout.addWidget(MyFigureCanvas(100,10,data_dict,"Carbon5",230,330),3,3)
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
        

        self.moveLabel.mouseMoveEvent = self.moveWindow
        
        self.moveLabel.mousePressEvent = self.mousePressEvent
        
        
        
        #---------------------------------------------------------------------------------------
        
        #connect--controller--buttons---------------------------------------------------------------
        
        self.shovelUpButton.clicked.connect(self.Shovel_Up)
        
        self.shovelDownButton.clicked.connect(self.Shovel_Down)
        
        self.setShovelContainerPositionButton.clicked.connect(self.Set_Shovel_Container_Position)
        
        self.shovelTakeButton.clicked.connect(self.Outer_Shovel_Take)
        
        self.shovelPutButton.clicked.connect(self.Outer_Shovel_Put)
        
        self.setShovelPositionButton.clicked.connect(self.Set_Outer_Shovel_Position)
        
        self.soilTakerOpenButton.clicked.connect(self.Inner_Shovel_Take)
        
        self.soilTakerCloseButton.clicked.connect(self.Inner_Shovel_Put)
        
        self.setSoilTakerPositionButton.clicked.connect(self.Set_Inner_Shovel_Position)
        
        self.pump1StartButton.clicked.connect(self.WaterPump1_Pump)
        
        self.pump1StopButton.clicked.connect(self.WaterPump1_Stop)
        
        self.pump2StartButton.clicked.connect(self.WaterPump2_Pump)
        
        self.pump2StopButton.clicked.connect(self.WaterPump2_Stop)
        
        self.pump3StartButton.clicked.connect(self.WaterPump3_Pump)
        
        self.pump3StopButton.clicked.connect(self.WaterPump3_Stop)
        
        self.pump4StartButton.clicked.connect(self.WaterPump4_Pump)
        
        self.pump4StopButton.clicked.connect(self.WaterPump4_Stop)
        
        self.pumpAllButton.clicked.connect(self.WaterPumpAll_Pump)
        
        self.stopAllButton.clicked.connect(self.WaterPumpAll_Stop)
        
        self.tube1Button.clicked.connect(self.Tube_1)
        
        self.tube2Button.clicked.connect(self.Tube_2)
        
        self.tube3Button.clicked.connect(self.Tube_3)
        
        self.tube4Button.clicked.connect(self.Tube_4)
        
        self.setTubePositionButton.clicked.connect(self.Set_Tube_Position)
        
        self.takeCurrentPosition2TestPositionButton.clicked.connect(self.Take_Current_Tube_To_Test_Position)
        
        self.takeSelectedTube2TestPositionButton.clicked.connect(self.Take_Chosen_Tube_To_Test_Position)
        
        self.startAutoScienceButton.clicked.connect(self.Auto_Start)
        
        self.onlySoilTakingButton.clicked.connect(self.Take_Soil)
        
        self.putSoilButton.clicked.connect(self.Put_Soil)
        
        
        #--------------------------------------------------------------------------------------------
        
        
        #Line-Edit--------------------------------------------------------------------------------------
        
        # read only line edits
        # initial parameters for  Line edits
        self.statusLineEdit.setText("Unkown")
        self.currentShovelContainerPositionLineEdit.setText("Unkown")
        self.currentShovelPositionLineEdit.setText("Unkown")
        self.currentSoilTakerPositionLineEdit.setText("Unkown")
        self.currentTubePositionLineEdit.setText("Unkown") 
        ## Upper ones actually a label :D
        self.setShovelContainerPositionLineEdit.setText("Unkown")
        self.setShovelPositionLineEdit.setText("Unkown")
        self.setSoilTakerPositionLineEdit.setText("Unkown")
        self.setTubePositionLineEdit.setText("Unkown")
        self.takeTubeLineEdit.setText("Unkown")
        
        
        
        
        
        
        
        
        #-------------------------------------------------------------------------------------------------
        
    
    def moveWindow(self,event):
            # Detect if the window is  normal size
            # ###############################################  
            if self.isMaximized() == False: #Not maximized
                # Move window only when window is normal size  
                # ###############################################
                #if left mouse button is clicked (Only accept left mouse button clicks)
                if (event.buttons() == QtCore.Qt.LeftButton):  
                    #Move window 
                    self.move(self.pos() + event.globalPos() - self.clickPosition)
                    self.clickPosition = event.globalPos()
                    event.accept()
                    
                    
    def mousePressEvent(self,event):
         self.clickPosition = event.globalPos()
         print(self.clickPosition)
         print("  ")
         print(event.globalPos())
      
       
    
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
            self.graphGridLayout.addWidget(self.myFig3,1,3)
            
            self.myFig4 = MyFigureCanvas(100,10,data_dict,"Carbon",230,330)
            self.graphGridLayout.addWidget(self.myFig4,2,1)
            
            self.myFig5 = MyFigureCanvas(100,10,data_dict,"Carbon1",230,330)
            self.graphGridLayout.addWidget(self.myFig5,2,2)
            
            self.myFig6 = MyFigureCanvas(100,10,data_dict,"Carbon2",230,330)
            self.graphGridLayout.addWidget(self.myFig6,2,3)
            
            self.myFig7 = MyFigureCanvas(100,10,data_dict,"Carbon3",230,330)
            self.graphGridLayout.addWidget(self.myFig7,3,1)
            
            self.myFig8 = MyFigureCanvas(100,10,data_dict,"Carbon4",230,330)
            self.graphGridLayout.addWidget(self.myFig8,3,2)
            
            self.myFig9 = MyFigureCanvas(100,10,data_dict,"Carbon5",230,330)
            self.graphGridLayout.addWidget(self.myFig9,3,3)
            
        elif index ==1:
            self.ClearLayout(self.graphGridLayout)
            self.myFig1 =MyFigureCanvas(100,10,data_dict,"Temperature",10,40)
            self.graphGridLayout.addWidget(self.myFig1)
            
            
        elif index ==2:
            self.ClearLayout(self.graphGridLayout)
            self.myFig2 = MyFigureCanvas(100,10,data_dict,"Pressure",150,350)
            self.graphGridLayout.addWidget(self.myFig2)
            
        elif index ==3:
            self.ClearLayout(self.graphGridLayout)
            self.myFig3 = MyFigureCanvas(100,10,data_dict,"Altitude",2980,3110)
            self.graphGridLayout.addWidget(self.myFig3)
            
        elif index ==4:
            self.ClearLayout(self.graphGridLayout)
            self.myFig4 = MyFigureCanvas(100,10,data_dict,"Carbon",230,330)
            self.graphGridLayout.addWidget(self.myFig4)
            
        elif index ==5:
            self.ClearLayout(self.graphGridLayout)
            self.myFig5 = MyFigureCanvas(100,10,data_dict,"Carbon1",230,330)
            self.graphGridLayout.addWidget(self.myFig5)
            
        elif index ==6:
            self.ClearLayout(self.graphGridLayout)
            self.myFig6 = MyFigureCanvas(100,10,data_dict,"Carbon2",230,330)
            self.graphGridLayout.addWidget(self.myFig6)
            
        elif index ==7:
            self.ClearLayout(self.graphGridLayout)
            self.myFig7 = MyFigureCanvas(100,10,data_dict,"Carbon3",230,330)
            self.graphGridLayout.addWidget(self.myFig7)
            
        elif index ==8:
            self.ClearLayout(self.graphGridLayout)
            self.myFig8 = MyFigureCanvas(100,10,data_dict,"Carbon4",230,330)
            self.graphGridLayout.addWidget(self.myFig8)
            
        elif index ==9:
            self.ClearLayout(self.graphGridLayout)
            self.myFig9 = MyFigureCanvas(100,10,data_dict,"Carbon5",230,330)
            self.graphGridLayout.addWidget(self.myFig9)
            
        
        
            
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
            
    
    
    #----ButtonFunctions--------------------------------------------------------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    def Outer_Shovel_Take(self):
        if (self.isSoilTakenByOuterShovel == False):
            self.message = 0
            self.OuterShovel.publish(self.message)
            self.isSoilTakenByOuterShovel = True
            
            self.currentStatus = "Taking sample from soil"
            self.RoverListener(self.currentStatus)
            

    def Outer_Shovel_Put(self):
        if(self.isSoilTakenByOuterShovel):
            self.message = 1
            self.OuterShovel.publish(self.message)
            self.isSoilTakenByOuterShovel = False
            self.currentStatus = "Pouring Sample"
            self.RoverListener(self.currentStatus)
            
            
    def Inner_Shovel_Take(self):
        if (self.isSoilTakenByInnerShovel ==False and self.isShovelContainerDown == False):
            self.message = 0
            self.InnerShovel.publish(self.message)
            self.isSoilTakenByInnerShovel = True
            self.currentStatus = "Inner shovel preapearing to take sample"
            self.RoverListener(self.currentStatus)
            

    def Inner_Shovel_Put(self):
        if(self.isSoilTakenByInnerShovel):
            self.message = 1
            self.InnerShovel.publish(self.message)
            self.isSoilTakenByInnerShovel = False
            self.currentStatus = "Inner shovel is pouring the sample into Tube :  " + str(self.currentPositionTube)
            self.RoverListener(self.currentStatus)
            


    def Shovel_Up(self):
        if(self.isShovelContainerDown):
            self.message = 200*(360/8)
            self.isShovelContainerDown = False
            self.ShovelUp.publish(self.message)
            self.currentStatus = "Shovel goes UP"
            self.RoverListener(self.currentStatus)
    def Shovel_Down(self):
        if self.currentPositionTube != 0:
            self.Tube_4()
            
            if (self.isShovelContainerDown == False):
                self.message =  200*(360/8)
                self.isShovelContainerDown = True
                self.ShovelDown.publish(self.message)
                self.currentStatus = "Shovel goes Down"
                self.RoverListener(self.currentStatus)
        
    
    def Tube_1(self):
        if self.isShovelContainerDown == False: 
            self.destination = 1
            self.message = abs((self.currentPositionTube - self.destination)) * 574/4  
            self.currentPositionTube = 1
            self.Tubes.publish(self.message)
            self.currentStatus = "Switching to Tube 1"
            self.RoverListener(self.currentStatus)


    def Tube_2(self):
        if self.isShovelContainerDown == False: 
            self.destination = 2
            self.message = abs((self.currentPositionTube - self.destination)) * 574/4  
            self.currentPositionTube = 2
            self.Tubes.publish(self.message)
            self.currentStatus = "Switching to Tube 2"
            self.RoverListener(self.currentStatus)

    def Tube_3(self):
        if self.isShovelContainerDown == False: 
            self.destination = 3
            self.message = abs((self.currentPositionTube - self.destination)) * 574/4  
            self.currentPositionTube = 3
            self.Tubes.publish(self.message)
            self.currentStatus = "Switching to Tube 3"
            self.RoverListener(self.currentStatus)

    def Tube_4(self):
        if self.isShovelContainerDown == False: 
            self.destination = 4
            self.message = abs((self.currentPositionTube - self.destination)) * 574/4  
            self.currentPositionTube = 0
            self.Tubes.publish(self.message)
            self.currentStatus = "Switching to Tube 4"
            self.RoverListener(self.currentStatus)
            
            
    def Set_Tube_Position(self):
        pos = self.setTubePositionLineEdit.text()
        pos = int(pos)
        x = self.currentPositionTube
        self.currentPositionTube = pos
        self.currentStatus = "Successfully changed tube position " + str(x) + " to " + str(self.currentPositionTube)
        self.statusLineEdit.setText(self.currentStatus)
        self.currentTubePositionLineEdit.setText(str(self.currentPositionTube))
        
    def Set_Shovel_Container_Position(self):
        boolPos = self.setShovelContainerPositionLineEdit.text()
        if(boolPos == "DOWN"):
            boolPos = True
        elif (boolPos == "UP"):
            boolPos = False
        else:
            boolPos = self.isShovelContainerDown
        x = self.isShovelContainerDown
        self.isShovelContainerDown = boolPos
        
        if (x == False):
            x = "UP"
            
        else:
            x="DOWN"
            
        if self.isShovelContainerDown == True:
            c = "DOWN"
            
        else:
            c ="UP"
            
            
        self.currentStatus = "Successfully changed shovel container position " + x + " to " + c
        self.statusLineEdit.setText(self.currentStatus)
        self.currentShovelContainerPositionLineEdit.setText(c)
        
    def Set_Outer_Shovel_Position(self):
        boolPos = self.setShovelPositionLineEdit.text()
        if(boolPos == "0"):
            boolPos = True
        elif (boolPos == "1"):
            boolPos = False
        else:
            boolPos = self.isSoilTakenByOuterShovel
        
        x =   self.isSoilTakenByOuterShovel
        self.isSoilTakenByOuterShovel = boolPos
        
        self.currentStatus = "Successfully changed shovel container position " + str(x) + " to " + str( self.isSoilTakenByOuterShovel)
        self.statusLineEdit.setText(self.currentStatus)
        self.currentShovelPositionLineEdit.setText(str(boolPos))
        
    
    def Set_Inner_Shovel_Position(self):
        boolPos = self.setSoilTakerPositionLineEdit.text()
        if(boolPos == "0"):
            boolPos = True
        elif (boolPos == "1"):
            boolPos = False
        else:
            boolPos = self.isSoilTakenByInnerShovel
        x = self.isSoilTakenByInnerShovel
        self.isSoilTakenByInnerShovel = boolPos
        
        self.currentStatus = "Successfully changed shovel container position " + str(x) + " to " + str( self.isSoilTakenByInnerShovel)
        self.statusLineEdit.setText(self.currentStatus)
        self.currentSoilTakerPositionLineEdit.setText(str(boolPos))
    
    def Take_Current_Tube_To_Test_Position(self):
        if self.isShovelContainerDown == False: 
            self.destination = self.testPosition
            self.message = abs((self.currentPositionTube - self.destination)) * 574/4  
            self.currentPositionTube = self.testPosition
            self.Tubes.publish(self.message)
            self.currentStatus = f"Taking current tube {self.currentPositionTube} to test position {self.testPosition}" 
            self.RoverListener(self.currentStatus)
            
    
    def Take_Chosen_Tube_To_Test_Position(self):
        if self.isShovelContainerDown == False: 
            chosenOne = self.takeTubeLineEdit.text()
            chosenOne = int(chosenOne)
            self.destination = self.testPosition
            self.message = abs((chosenOne - self.destination)) * 574/4  
            self.currentPositionTube = self.testPosition
            self.Tubes.publish(self.message)
            self.currentStatus = f"Taking chosen tube {chosenOne} to test position {self.testPosition}" 
            self.RoverListener(self.currentStatus)
        
        
    
        

    def WaterPump1_Pump(self):
        self.message = 1
        self.WaterPumps.publish(self.message)
        self.currentStatus = "Pumping pump 1"
        self.RoverListener(self.currentStatus)
        

    def WaterPump1_Stop(self):
        self.message = 0
        self.WaterPumps.publish(self.message)
        self.currentStatus = "Stoping pump 1"
        self.RoverListener(self.currentStatus)
        
    def WaterPump2_Pump(self):
        self.message = 3
        self.WaterPumps.publish(self.message)
        self.currentStatus = "Pumping pump 2"
        self.RoverListener(self.currentStatus)
        

    def WaterPump2_Stop(self):
        self.message = 2
        self.WaterPumps.publish(self.message) 
        self.currentStatus = "Stoping pump 2"
        self.RoverListener(self.currentStatus)
    def WaterPump3_Pump(self):
        self.message = 5
        self.WaterPumps.publish(self.message)
        self.currentStatus = "Pumping pump 3"
        self.RoverListener(self.currentStatus)
        

    def WaterPump3_Stop(self):
        self.message = 4
        self.WaterPumps.publish(self.message) 
        self.currentStatus = "Stoping pump 3"
        self.RoverListener(self.currentStatus)
    def WaterPump4_Pump(self):
        self.message = 7
        self.WaterPumps.publish(self.message)
        self.currentStatus = "Pumping pump 4"
        self.RoverListener(self.currentStatus)
        

    def WaterPump4_Stop(self):
        self.message = 6
        self.WaterPumps.publish(self.message) 
        self.currentStatus = "Stoping pump 4"
        self.RoverListener(self.currentStatus)
    def WaterPumpAll_Pump(self):
        self.message = 9
        self.WaterPumps.publish(self.message)
        self.currentStatus = "Pumping pump all"
        self.RoverListener(self.currentStatus)
        

    def WaterPumpAll_Stop(self):
        self.message = 8
        self.WaterPumps.publish(self.message)
        self.currentStatus = "Stoping pump all"
        self.RoverListener(self.currentStatus)
        
    def RoverListener(self,currentStatus):
        
        value = 0 # this will listen to rover and continues 
        
        k = 1
        while (True):
            if (value == 0):
                string = currentStatus +"."*k
                self.statusLineEdit.setText(string)
                k+=1
                
                if (k>3):
                    k =1
                    
                
                
                time.sleep(0.5)
            elif value ==1:
                break
            
    
    def Auto_Start(self):
        if (self.pressedAutoFunction == False):
            
            self.pressedAutoFunction = True
            
            self.Shovel_Down()
            
            self.Outer_Shovel_Take()
            
            
            
            self.Shovel_Up()
            
            
            
            self.Inner_Shovel_Take()
            
          
            
            self.Outer_Shovel_Put()
            
          
            
            self.Inner_Shovel_Put()
            
           
            
            self.Take_Current_Tube_To_Test_Position()
            
           
            
            self.Take_Current_Tube_To_Test_Position()
            
        
            
            self.pressedAutoFunction = False
    
    
    def Take_Soil(self):
        if (self.pressedAutoFunction == False):
            
            self.pressedAutoFunction = True
            
            self.Shovel_Down()
            
            self.Outer_Shovel_Take()
          
            
            self.pressedAutoFunction = False
        
    def Put_Soil(self):
         if (self.pressedAutoFunction == False):
            
            self.Shovel_Up()
            
          
            
            self.Inner_Shovel_Take()
            
        
            
            self.Outer_Shovel_Put()
            
          
            
            self.Inner_Shovel_Put()
            
         
            
            self.Take_Current_Tube_To_Test_Position()
       
            
            self.Take_Current_Tube_To_Test_Position()
            
     
            
            self.pressedAutoFunction = False
    
    
    
    
    
    #---------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------------------------------------------------------------------------

    
    
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
data_dict = {"Temperature":[1]*100,"Pressure":[1]*100,"Altitude":[1]*100,"Carbon":[1]*100,"Carbon1":[1]*100,"Carbon2":[1]*100,"Carbon3":[1]*100,"Carbon4":[1]*100,"Carbon5":[1]*100}


def Sensor_Call_Back(sensor_datas):
    data_list = sensor_datas.data.split(",")
    data_dict["Temperature"].append(float(data_list[0]))
    data_dict["Pressure"].append(float(data_list[1]))
    data_dict["Altitude"].append(float(data_list[2]))
    data_dict["Carbon"].append(float(data_list[3]))
    data_dict["Carbon1"].append(float(data_list[4]))
    data_dict["Carbon2"].append(float(data_list[5]))
    data_dict["Carbon3"].append(float(data_list[6]))
    data_dict["Carbon4"].append(float(data_list[7]))
    data_dict["Carbon5"].append(float(data_list[8]))
    
    
def randomFill():
    data_dict["Temperature"].append(float(random.randint(20,30)))
    data_dict["Pressure"].append(float(random.randint(200,300)))
    data_dict["Altitude"].append(float(random.randint(3000,3100)))
    data_dict["Carbon"].append(float(random.randint(250,300)))
    data_dict["Carbon1"].append(float(random.randint(250,300)))
    data_dict["Carbon2"].append(float(random.randint(250,300)))
    data_dict["Carbon3"].append(float(random.randint(250,300)))
    data_dict["Carbon4"].append(float(random.randint(250,300)))
    data_dict["Carbon5"].append(float(random.randint(250,300)))
    
    
#-----------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(open("Combinear.qss","r").read())
    
    mainWindow = SSGUI()
    mainWindow.show()
    sys.exit(app.exec_())
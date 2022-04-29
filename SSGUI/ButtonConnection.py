# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 07:57:07 2022

@author: LENOPC
"""

import time


class Button_Functions():
    
    def __init__(self):
        
        self.currentPositionTube = 0
        self.destinationTube = 0
        self.isShovelContainerDown = False
        self.isSoilTakenByOuterShovel = False
        self.isSoilTakenByInnerShovel = False
        self.testPosition = 0
        self.currentStatus = ""
        self.pressedAutoFunction = False;
        
        
        
    def Outer_Shovel_Take(self):
        if (self.isSoilTakenByOuterShovel == False):
            self.message = 0
            self.OuterShovel.publish(self.message)
            self.isSoilTakenByOuterShovel = True
            
            self.currentStatus = "Taking sample from soil"

    def Outer_Shovel_Put(self):
        if(self.isSoilTakenByOuterShovel):
            self.message = 1
            self.OuterShovel.publish(self.message)
            self.isSoilTakenByOuterShovel = False
            self.currentStatus = "Pouring Sample"
            
    def Inner_Shovel_Take(self):
        if (self.isSoilTakenByInnerShovel ==False and self.isShovelContainerDown == False):
            self.message = 0
            self.InnerShovel.publish(self.message)
            self.isSoilTakenByInnerShovel = True
            self.currentStatus = "Inner shovel preapearing to take sample"

    def Inner_Shovel_Put(self):
        if(self.isSoilTakenByInnerShovel):
            self.message = 1
            self.InnerShovel.publish(self.message)
            self.isSoilTakenByInnerShovel = False
            self.currentStatus = "Inner shovel is pouring the sample into Tube :  " + str(self.currentPositionTube)


    def Shovel_Up(self):
        if(self.isShovelContainerDown):
            self.message = 200*(360/8)
            self.isShovelContainerDown = False
            self.ShovelUp.publish(self.message)
            self.currentStatus = "Shovel goes UP"
    def Shovel_Down(self):
        if self.currentPositionTube != 0:
            self.Tube_4()
            
            if (self.isShovelContainerDown == False):
                self.message =  200*(360/8)
                self.isShovelContainerDown = True
                self.ShovelDown.publish(self.message)
                self.currentStatus = "Shovel goes Down"
        
    
    def Tube_1(self):
        if self.isShovelContainerDown == False: 
            self.destination = 1
            self.message = abs((self.currentPositionTube - self.destination)) * 574/4  
            self.currentPositionTube = 1
            self.Tubes.publish(self.message)
            self.currentStatus = "Switching to Tube 1"


    def Tube_2(self):
        if self.isShovelContainerDown == False: 
            self.destination = 2
            self.message = abs((self.currentPositionTube - self.destination)) * 574/4  
            self.currentPositionTube = 2
            self.Tubes.publish(self.message)
            self.currentStatus = "Switching to Tube 2"

    def Tube_3(self):
        if self.isShovelContainerDown == False: 
            self.destination = 3
            self.message = abs((self.currentPositionTube - self.destination)) * 574/4  
            self.currentPositionTube = 3
            self.Tubes.publish(self.message)
            self.currentStatus = "Switching to Tube 3"

    def Tube_4(self):
        if self.isShovelContainerDown == False: 
            self.destination = 4
            self.message = abs((self.currentPositionTube - self.destination)) * 574/4  
            self.currentPositionTube = 0
            self.Tubes.publish(self.message)
            self.currentStatus = "Switching to Tube 4"
            
            
    def Set_Tube_Position(self,pos):
        x = self.currentPositionTube
        self.currentPositionTube = pos
        self.currentStatus = "Successfully changed tube position " + str(x) + " to " + str(self.currentPositionTube)
        
    def Set_Shovel_Container_Position(self,boolPos):
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
        
    def Set_Outer_Shovel_Position(self,boolPos):
        x =   self.isSoilTakenByOuterShovel
        self.isSoilTakenByOuterShovel = boolPos
        
        self.currentStatus = "Successfully changed shovel container position " + str(x) + " to " + str( self.isSoilTakenByOuterShovel)
        
    
    def Set_Inner_Shovel_Position(self,boolPos):
        x = self.isSoilTakenByInnerShovel
        self.isSoilTakenByInnerShovel = boolPos
        
        self.currentStatus = "Successfully changed shovel container position " + str(x) + " to " + str( self.isSoilTakenByInnerShovel)
    
    
    def Take_Current_Tube_To_Test_Position(self):
        if self.isShovelContainerDown == False: 
            self.destination = self.testPosition
            self.message = abs((self.currentPositionTube - self.destination)) * 574/4  
            self.currentPositionTube = self.testPosition
            self.Tubes.publish(self.message)
            self.currentStatus = f"Taking current tube {self.currentPositionTube} to test position {self.testPosition}" 
            
    
    def Take_Chosen_Tube_To_Test_Position(self,chosenOne):
        if self.isShovelContainerDown == False: 
            self.destination = self.testPosition
            self.message = abs((chosenOne - self.destination)) * 574/4  
            self.currentPositionTube = self.testPosition
            self.Tubes.publish(self.message)
            self.currentStatus = f"Taking chosen tube {chosenOne} to test position {self.testPosition}" 
        
        
    
        

    def WaterPump1_Pump(self):
        self.message = 1
        self.WaterPumps.publish(self.message)
        self.currentStatus = "Pumping pump 1"
        

    def WaterPump1_Stop(self):
        self.message = 0
        self.WaterPumps.publish(self.message)
        self.currentStatus = "Stoping pump 1"
        
    def WaterPump2_Pump(self):
        self.message = 3
        self.WaterPumps.publish(self.message)
        self.currentStatus = "Pumping pump 2"
        

    def WaterPump2_Stop(self):
        self.message = 2
        self.WaterPumps.publish(self.message) 
        self.currentStatus = "Stoping pump 2"
    def WaterPump3_Pump(self):
        self.message = 5
        self.WaterPumps.publish(self.message)
        self.currentStatus = "Pumping pump 3"
        

    def WaterPump3_Stop(self):
        self.message = 4
        self.WaterPumps.publish(self.message) 
        self.currentStatus = "Stoping pump 3"
    def WaterPump4_Pump(self):
        self.message = 7
        self.WaterPumps.publish(self.message)
        self.currentStatus = "Pumping pump 4"
        

    def WaterPump4_Stop(self):
        self.message = 6
        self.WaterPumps.publish(self.message) 
        self.currentStatus = "Stoping pump 4"
    def WaterPumpAll_Pump(self):
        self.message = 9
        self.WaterPumps.publish(self.message)
        self.currentStatus = "Pumping pump all"
        

    def WaterPumpAll_Stop(self):
        self.message = 8
        self.WaterPumps.publish(self.message)
        self.currentStatus = "Stoping pump all"
        
    def RoverListener(self,currentStatus):
        
        value = 0 # this will listen to rover and continues 
        print(currentStatus)
        k = 1
        while (True):
            if (value == 0):
                string = currentStatus +"."*k
                print(string)
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
            
            self.RoverListener(self.currentStatus)
            
            self.Outer_Shovel_Take()
            
            self.RoverListener(self.currentStatus)
            
            self.Shovel_Up()
            
            self.RoverListener(self.currentStatus)
            
            self.Inner_Shovel_Take()
            
            self.RoverListener(self.currentStatus)
            
            self.Outer_Shovel_Put()
            
            self.RoverListener(self.currentStatus)
            
            self.Inner_Shovel_Put()
            
            self.RoverListener(self.currentStatus)
            
            self.Take_Current_Tube_To_Test_Position()
            
            self.RoverListener(self.currentStatus)
            
            self.Take_Current_Tube_To_Test_Position()
            
            self.RoverListener(self.currentStatus)
            
            self.pressedAutoFunction = False
    
    
    def Take_Soil(self):
        if (self.pressedAutoFunction == False):
            
            self.pressedAutoFunction = True
            
            self.Shovel_Down()
            
            self.RoverListener(self.currentStatus)
            
            self.Outer_Shovel_Take()
            
            self.RoverListener(self.currentStatus)
            
            self.pressedAutoFunction = False
        
    def Put_Soil(self):
         if (self.pressedAutoFunction == False):
            
            self.Shovel_Up()
            
            self.RoverListener(self.currentStatus)
            
            self.Inner_Shovel_Take()
            
            self.RoverListener(self.currentStatus)
            
            self.Outer_Shovel_Put()
            
            self.RoverListener(self.currentStatus)
            
            self.Inner_Shovel_Put()
            
            self.RoverListener(self.currentStatus)
            
            self.Take_Current_Tube_To_Test_Position()
            
            self.RoverListener(self.currentStatus)
            
            self.Take_Current_Tube_To_Test_Position()
            
            self.RoverListener(self.currentStatus)
            
            self.pressedAutoFunction = False
        
    







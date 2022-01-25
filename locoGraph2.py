#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rospy
import matplotlib.pyplot as plt
from std_msgs.msg import String

motor_dataL = {"velocity":[0],"voltage":[0],"temperature":[0],"current":[0]}

motor_dataR= {"velocity":[0],"voltage":[0],"temperature":[0],"current":[0]}

def plotting(data):
    data_list = data.data.split(";")
    
    motor_dataL["velocity"].append(float(data_list[0]))
    motor_dataL["voltage"].append(float(data_list[1]))
    motor_dataL["temperature"].append(float(data_list[2]))
    motor_dataL["current"].append(float(data_list[3]))
    motor_dataR["velocity"].append(float(data_list[4]))
    motor_dataR["voltage"].append(float(data_list[5]))
    motor_dataR["temperature"].append(float(data_list[6]))
    motor_dataR["current"].append(float(data_list[7]))


    if len(motor_dataL["velocity"]) <100:
        plt.subplot(4,1,1)
        plt.plot(motor_dataL["velocity"],color = "blue")
        plt.plot(motor_dataR["velocity"],color = "red")
        plt.ylabel("velocity")
        
        plt.subplot(4,1,2)
        plt.plot(motor_dataL["voltage"],color = "blue")
        plt.plot(motor_dataR["voltage"],color = "red")
        plt.ylabel("voltage")
        
        plt.subplot(4,1,3)
        plt.plot(motor_dataL["temperature"],color = "blue")
        plt.plot(motor_dataR["temperature"],color = "red")
        plt.ylabel("temperature")

        plt.subplot(4,1,4)
        plt.plot(motor_dataL["current"],color = "blue")
        plt.plot(motor_dataR["current"],color = "red")
        plt.ylabel("current")
        
        plt.draw()
        plt.pause(0.0001)
    else:
        plt.subplot(4,1,1)
        plt.plot(motor_dataL["velocity"][-100:],color = "blue")
        plt.plot(motor_dataR["velocity"][-100:],color = "red")
        plt.ylabel("velocity")
        
        plt.subplot(4,1,2)
        plt.plot(motor_dataL["voltage"][-100:],color = "blue")
        plt.plot(motor_dataR["voltage"][-100:],color = "red")
        plt.ylabel("voltage")
        
        plt.subplot(4,1,3)
        plt.plot(motor_dataL["temperature"][-100:],color = "blue")
        plt.plot(motor_dataR["temperature"][-100:],color = "red")
        plt.ylabel("temperature")

        plt.subplot(4,1,4)
        plt.plot(motor_dataL["current"][-100:],color = "blue")
        plt.plot(motor_dataR["current"][-100:],color = "red")
        plt.ylabel("current")
        
        plt.draw()
        plt.pause(0.0001)
    



if __name__ == '__main__' :
    
	rospy.init_node('graph' , anonymous=True)
	rospy.Subscriber('chatter', String , plotting)
	plt.show()
	rospy.spin()

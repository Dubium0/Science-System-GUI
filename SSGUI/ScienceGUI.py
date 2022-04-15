# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 22:43:23 2022

@author: LENOPC
"""

import sys

from PyQt5.QtWidgets import QApplication,QWidget , QVBoxLayout


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.window_width, self.window_height, = 1200,800
        self.setMinimumSize(self.window_width,self.window_height)
        layout  = QVBoxLayout()
        self.setLayout(layout)
        
    
    
    
if __name__ =='__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(open("theme.qss","r").read())
    myApp = MyApp()
    myApp.show()
    
    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Windows ')
        
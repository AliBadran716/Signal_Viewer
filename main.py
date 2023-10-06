#PyQr5 importing
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType #Live updating the design

import os
from os import path
import sys

FORM_CLASS,_ = loadUiType(path.join(path.dirname(__file__), "main.ui")) # connects the Ui file with the Python file

class MainApp (QMainWindow,FORM_CLASS): # go to the main window in the form_class file
    def __init__(self,parent=None): #constructor to intiate the main window  in the design
        super(MainApp,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handle_btn()

    def Handle_btn(self):
        self.graph1_radio_btn.toggled.connect(self.graph1_selected)
        self.graph2_radio_btn.toggled.connect(self.graph2_selected)
        self.link_radio_btn.toggled.connect(self.link_selected)
        self.speed_push_btn.clicked.connect(self.speed_changed)
        self.play_push_btn.clicked.connect(self.play_changed)
        self.rewind_push_btn.clicked.connect(self.rewind_changed)

    def graph1_selected(self, enabled):
        if enabled:
            print('graph1')
    def graph2_selected(self, enabled):
        if enabled:
            print('graph2')

    def link_selected(self, enabled):
        if enabled:
            print('link')

    def speed_changed(self):
        print("speed change")

    def play_changed(self,state):
        print("play")


    def rewind_changed(self):
        print("rewind")



def main() : #method to start app
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_() #infinte Loop

if __name__ == '__main__':
    main()
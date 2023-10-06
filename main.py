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

    







def main() : #method to start app
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_() #infinte Loop

if __name__ == '__main__':
    main()
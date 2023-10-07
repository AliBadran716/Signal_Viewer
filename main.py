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
        self.hide_g1_check_btn.stateChanged.connect(self.hide_g1_btn_checked)
        self.hide_g2_check_btn.stateChanged.connect(self.hide_g2_btn_checked)
        self.color_g1_combo_btn.activated[str].connect(self.color_g1_combo_selected)
        self.save_lbl_g1_btn.clicked.connect(self.line_edit_g1_selected)
        self.zoom_slider.valueChanged.connect(self.zoom_slider_update)
        self.move_x_slider.valueChanged.connect(self.move_x_slider_update)
        self.move_y_slider.valueChanged.connect(self.move_y_slider_update)
        self.tab_widget_g1.currentChanged.connect(self.tab_widget_g1_changed)
        self.tab_widget_g2.currentChanged.connect(self.tab_widget_g2_changed)
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

    def zoom_slider_update(self):
        value = self.zoom_slider.value()
        self.label.setText(f"Value: {value}")
        print(value)

    def move_x_slider_update(self):
        value = self.move_x_slider.value()
        self.label.setText(f"Value: {value}")
        print(value)

    def move_y_slider_update(self):
        value = self.move_y_slider.value()
        self.label.setText(f"Value: {value}")
        print(value)

    def tab_widget_g1_changed(self):
        current_tab = self.tab_widget_g1.currentIndex()
        print(current_tab)

    def tab_widget_g2_changed(self):
        current_tab = self.tab_widget_g2.currentIndex()
        print(current_tab)

    def hide_g1_btn_checked(self):
        if self.hide_g1_check_btn.isChecked() == True:
            print("checked")

        else:
            print("unchecked")

    def hide_g2_btn_checked(self):
        if self.hide_g2_check_btn.isChecked() == True:
            print("checked")

        else:
            print("unchecked")

    def color_g1_combo_selected(self, text):
        print(text)

    def line_edit_g1_selected(self):
        print(self.line_edit_g1.text())




def main() : #method to start app
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_() #infinte Loop

if __name__ == '__main__':
    main()
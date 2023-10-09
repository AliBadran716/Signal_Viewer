# PyQt5 importing
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType  # Live updating the design

import pyqtgraph as pg
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
_translate = QtCore.QCoreApplication.translate

from pyqtgraph import PlotWidget, plot
from PyQt5.QtWidgets import QFileDialog, QGraphicsScene
import numpy as np
import pandas as pd
from PyQt5.QtGui import QImageWriter
from io import BytesIO


from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

import os
from os import path
import sys

FORM_CLASS, _ = loadUiType(path.join(path.dirname(__file__), "main.ui"))  # connects the Ui file with the Python file


class MainApp(QMainWindow, FORM_CLASS):  # go to the main window in the form_class file

    def __init__(self, parent=None):  # constructor to intiate the main window  in the design
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        num_tabs = 1
        self.setupUi(self)
        self.Handle_btn()
        self.shortcuts()
        #A dict to save the data of all signals as pairs of keys and values, the key is a counter for the signals 
        # the value is a list that contains the data of each signal in the form of :
        #[[x_values], [y_values], [color_of signal], label_of_signal, is_hide, file_name]
        self.signals_data = {}
        
        self.count_signals = 0;
        self.end_indx = 50
        self.start_1 = 0
        self.end = 0.154
        self.is_playing = True
        self.loaddata()
        self.file_names = []
        self.speeds = ["x1", "x1.25", "x1.5", "x2"]
        self.current_speed_index = 0
        self.speed_push_btn.setText(self.speeds[self.current_speed_index])
        self.loaddata()

    def Handle_graph(self , file_names ):
        #self.graphicsView = PlotWidget(self.widget)
        colors = [(255,0,0),(0,255,0),(0,0,255)]
        self.graphicsView.setObjectName("graphicsView")
        self.data_lines = []
        #list_df = []
        self.graphicsView.setXRange(0, 0.154)
        self.graphicsView.setYRange(-1, 1)
        self.graphicsView.setBackground('w')
        #file_names = ['normal_ecg.csv','normal_emg.csv' , 'normal_rsp.csv']
        for i,file_name in enumerate(file_names):
           
           df = pd.read_csv(file_name)
        #list_df.append(pd.read_csv(file_name))
           x = df.iloc[:, 0].tolist()
        #self.x = list(range(100))  # 100 time points
        #self.y = [randint(0, 100) for _ in range(100)]  # 100 data points
           y = df.iloc[:, 1].tolist()
           pen = pg.mkPen(color=colors[i])
           data_line = self.graphicsView.plot(x, y, pen=pen)
           data_line.x_data = x
           data_line.y_data = y
           self.data_lines.append(data_line)
           print(len(self.data_lines))
        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

    def update_plot_data(self  ):
        for data_line in self.data_lines:
            self.end_indx+=4
            if(self.end_indx>=400 and self.end_indx<2560):
                self.start_1 = self.start_1 + 0.001
                self.end = self.end + 0.001 
            
            x_data = data_line.x_data[:self.end_indx]
            
            y_data = data_line.y_data[:self.end_indx]
            if (self.end_indx <= 500 ):
                self.graphicsView.setXRange(0, 0.154)
            else:
             if(self.end_indx > 500):
                self.graphicsView.setXRange(self.start_1, self.end)

            if(self.end_indx == 2560):
              self.timer.stop()
            data_line.setData(x_data, y_data)


    def Handle_btn(self):
        # menu buttons
        self.open_menu_btn.triggered.connect(self.add_new_signal)
        self.make_pdf_btn.triggered.connect(self.capture_and_create_pdf)
        # graph buttons
        self.graph1_radio_btn.toggled.connect(self.graph1_selected)
        self.graph2_radio_btn.toggled.connect(self.graph2_selected)
        self.link_radio_btn.toggled.connect(self.link_selected)
        self.speed_push_btn.clicked.connect(self.speed_changed)
        self.play_pause_btn.clicked.connect(self.play_pause)
        self.rewind_push_btn.clicked.connect(self.rewind_changed)
        self.zoom_slider.valueChanged.connect(self.zoom_slider_update)
        self.move_x_slider.valueChanged.connect(self.move_x_slider_update)
        self.move_y_slider.valueChanged.connect(self.move_y_slider_update)
        # signal buttons
        self.hide_g1_check_btn.stateChanged.connect(self.hide_g1_btn_checked)
        self.hide_g2_check_btn.stateChanged.connect(self.hide_g2_btn_checked)
        self.color_g1_combo_btn.activated[str].connect(self.color_combo_selected)
        self.color_g2_combo_btn.activated[str].connect(self.color_combo_selected)
        self.save_lbl_g1_btn.clicked.connect(self.save_changes_g1)
        self.save_lbl_g2_btn.clicked.connect(self.save_changes_g2)
        self.comboBox.currentIndexChanged.connect(self.on_combobox_selection)

    # A Function  that defines some shortcuts to make the work with our app more easier
    def shortcuts(self):
        # defining shortcuts
        self.sc_open = QShortcut(QKeySequence('Ctrl+O'), self)
        self.sc_export = QShortcut(QKeySequence('Ctrl+E'), self)
        self.sc_g1 = QShortcut(QKeySequence('Ctrl+1'), self)
        self.sc_g2 = QShortcut(QKeySequence('Ctrl+2'), self)
        self.sc_link = QShortcut(QKeySequence('Ctrl+L'), self)
        self.sc_speed = QShortcut(QKeySequence('Ctrl+S'), self)
        self.sc_play = QShortcut(QKeySequence(' '), self)
        self.sc_rewind = QShortcut(QKeySequence('Ctrl+R'), self)

        # activating shortcuts
        self.sc_open.activated.connect(self.add_new_signal)
        self.sc_g1.activated.connect(self.graph1_selected)
        self.sc_export.activated.connect(self.capture_and_create_pdf)

        self.sc_g2.activated.connect(self.graph2_selected)
        self.sc_link.activated.connect(self.link_selected)
        self.sc_speed.activated.connect(self.speed_changed)
        self.sc_play.activated.connect(self.play_pause)
        self.sc_rewind.activated.connect(self.rewind_changed)




    #A function to let the user load the signal file, create another signal element in the dictionary, and send the file to the graph
    def add_new_signal(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if file_path:
            self.count_signals += 1
            file_name = file_path.split("/")[-1]
            self.file_names.append(file_name)
        #print(file_name)
            signal_data = pd.read_csv(file_name)
        #print(signal_data)
            time_column = signal_data.iloc[:, 0]  
            values_column = signal_data.iloc[:, 1]  
        # Convert the extracted columns to lists 
            time_values = time_column.tolist()
            v_values = values_column.tolist()
        # print(time_values)
        # print(v_values)
            #print(self.count_signals)
            self.signals_data[self.count_signals] = [time_values,v_values, 'Red',f"{'Signal'} - {self.count_signals}",False, file_name]
            print(self.signals_data[self.count_signals][3])
            self.comboBox.addItem(f"{'Signal'} - {self.count_signals}")
        self.Handle_graph(self.file_names)
    

    # A function that displays the data of the siganl based on which signal has been selected from the comboBox
    def on_combobox_selection(self):
        selected_item_index = self.comboBox.currentIndex()
        print(selected_item_index)
        self.color_g1_combo_btn.setCurrentText(self.signals_data[selected_item_index][2])
        self.line_edit_g1.setText(self.signals_data[selected_item_index][3])
        self.hide_g1_check_btn.setChecked(self.signals_data[selected_item_index][4])

        print(self.signals_data[selected_item_index][2])
        

    #A function that update the data of the signal whenever the user change the data and press on save button
    def save_changes_g1(self):
        selected_item_index = self.comboBox.currentIndex()
        label_text = self.line_edit_g1.text()
        # Get the selected color from the ComboBox
        selected_color = self.color_g1_combo_btn.currentText()
        checkbox_checked = self.hide_g1_check_btn.isChecked()
        self.signals_data[selected_item_index][2] = selected_color
        self.signals_data[selected_item_index][3] = label_text
        self.signals_data[selected_item_index][4] = checkbox_checked
        #print(self.signals_data[selected_item_index][2])
        #print(self.signals_data[selected_item_index][3])
        #print(self.signals_data[selected_item_index][4])
        #print(checkbox_checked)
        #print(selected_color)    

    def capture_and_create_pdf(self):
        # Create a PDF
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        # Prompt the user to choose the destination directory and file name
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Save PDF")
        file_dialog.setFileMode(QFileDialog.AnyFile)
        file_dialog.setNameFilter("PDF files (*.pdf)")
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)

        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()

            if selected_files:
                pdf_filename = selected_files[0]

                if not pdf_filename.lower().endswith(".pdf"):
                    # Ensure the file has a .pdf extension
                    pdf_filename += ".pdf"

                # Create a PDF file
                pdf_buffer = BytesIO()
                pdf_canvas = canvas.Canvas(pdf_buffer, pagesize=letter)

                # Save the captured image to a temporary file
                temp_image_path = "temp_image.png"
                plot_widget_image = QImage(self.graphicsView.size(), QImage.Format_ARGB32)
                plot_widget_image.fill(Qt.transparent)
                painter = QPainter(plot_widget_image)
                self.graphicsView.render(painter)
                painter.end()
                plot_widget_image.save(temp_image_path)

                # Add the captured image to the PDF
                x_position = 50  # Adjust this value to set the horizontal position
                y_position = 300  # Adjust this value to set the vertical position
                pdf_canvas.drawImage(temp_image_path, x_position, y_position)

                # Add a comment or text annotation to the PDF
                comment_x = 100  # Adjust this value to set the horizontal position of the comment
                comment_y = 200  # Adjust this value to set the vertical position of the comment
                comment_text = "----------------"
                pdf_canvas.drawString(comment_x, comment_y, comment_text)

                # Show the page and save the PDF
                pdf_canvas.showPage()
                pdf_canvas.save()

                # Close and save the PDF file
                with open(pdf_filename, "wb") as f:
                    f.write(pdf_buffer.getvalue())

                # Delete the temporary image file
                os.remove(temp_image_path)

                print(f'PDF with captured image and comment saved as {pdf_filename}')
    def graph1_selected(self ):
       
            print('graph1')

    def graph2_selected(self):
 
            print('graph2')

    def link_selected(self):
   
            print('link')

    def speed_changed(self):
        if (self.current_speed_index == 3):
            self.speed_push_btn.setText(self.speeds[0])
            self.current_speed_index = 0
        else :    
            self.current_speed_index = self.current_speed_index + 1
            self.speed_push_btn.setText(self.speeds[self.current_speed_index])
        

    #A function that triggers between play and pause to control the flow of signals on graph
    def play_pause(self):
        self.is_playing = not self.is_playing
        if self.is_playing:
            self.timer.start()
            #print('start')
       
        else:
            self.timer.stop()
            #print('stop')
        

    def rewind_changed(self):
        print("rewind")

    def zoom_slider_update(self):
        value = self.zoom_slider.value()
        print(value)

    def move_x_slider_update(self):
        value = self.move_x_slider.value()
        print(value)

    def move_y_slider_update(self):
        value = self.move_y_slider.value()
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

    def color_combo_selected(self, text):
        print(text)

   


    def save_changes_g2(self):
        print(self.line_edit_g2.text())

    def loaddata(self):
        signal = {
            "mean": "----",
            "std": "----",
            "duration": "----",
            "min": "----",
            "max": "----"
        }

        self.tableWidget.setColumnCount(len(signal))

        column = 0
        for key, value in signal.items():
            self.tableWidget.setItem(0, column, QtWidgets.QTableWidgetItem(value))
            self.tableWidget.setItem(1, column, QtWidgets.QTableWidgetItem(value))
            self.tableWidget.setItem(2, column, QtWidgets.QTableWidgetItem(value))
            self.tableWidget.setItem(3, column, QtWidgets.QTableWidgetItem(value))
            self.tableWidget.setItem(4, column, QtWidgets.QTableWidgetItem(value))
            column += 1    

def main():  # method to start app
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()  # infinte Loop


if __name__ == '__main__':
    main()

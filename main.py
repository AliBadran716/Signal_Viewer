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
from PyQt5.QtGui import QPixmap

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

from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors  # Add this import
from reportlab.lib.styles import getSampleStyleSheet
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.uic import loadUiType
from PyQt5.QtCore import QCoreApplication
from pyqtgraph import PlotWidget

from reportlab.lib.pagesizes import inch
# Other imports...
from reportlab.lib.pagesizes import letter, inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from reportlab.pdfgen import canvas
from reportlab.platypus import Spacer

import sys
import os
from io import BytesIO
import numpy as np
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Image, Table, TableStyle, PageBreak, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors



from io import BytesIO

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

import os
from os import path

class MainApp(QMainWindow, FORM_CLASS):  # go to the main window in the form_class file

    def __init__(self, parent=None):  # constructor to intiate the main window  in the design
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        num_tabs = 1
        self.setupUi(self)
        self.Handle_btn()
        self.shortcuts()
        self.selected_item_index = 0 
        #A dict to save the data of all signals as pairs of keys and values, the key is a counter for the signals 
        # the value is a list that contains the data of each signal in the form of :
        #[[x_values], [y_values], [color_of signal], label_of_signal, is_hide, file_name]
        self.signals_data_1 = {}
        self.signals_data_2 = {}
        self.graphicsView_1.setBackground('w')
        self.graphicsView_2.setBackground('w')
        self.count_signals_1 = 0;
        self.count_signals_2 = 0;
        self.end_indx_1 = 50
        self.end_indx_2 = 50
        self.start_1 = 0
        self.start_2 = 0
        self.end_1 = 0.154
        self.end_2 = 0.154
        self.is_playing_g_1 = True
        self.is_playing_g_2 = True
        self.loaddata()
        self.file_names = []
        self.speeds = ["x1", "x1.25", "x1.5", "x2"]
        self.current_speed_index = 0
        self.speed_push_btn.setText(self.speeds[self.current_speed_index])
        self.loaddata()
        self.colors = []
        self.hide_signals = []
        self.flag_1 = False
        self.flag_2 = False
        self.max_y=0
        self.graph_1_active = False
        self.graph_2_active = False
        self.max_x = 0
        self.number_of_points = 0
        self.start_flag = False
        self.flag_of_speed = False
        self.start_new = []    
        #self.flag_2 = False
        self.pdf_content = []
        self.snapshot_path=''
        self.snapshot_counter = 0
        self.title_pdf()
    


    def max_range_1 (self):
        for value in self.signals_data_1.values():
            #print(value[1])
            for search in value[1]:
               if(search > self.max_y):
                  self.max_y = search

    def max_range_2 (self):
        for value in self.signals_data_2.values():
            #print(value[1])
            for search in value[1]:
               if(search > self.max_y):
                  self.max_y = search

    def color_detect_1(self , signals_data_1):
        self.colors = []
        for value in signals_data_1.values():
            if(value[2] == 'Red'):
                self.colors.append((255 , 0 , 0))
            if (value[2] == 'Blue'):
                self.colors.append( (0 , 0, 255)) 
            if (value[2] == 'Green'):
                self.colors.append((0 , 250 , 0))       
                #print('colors')
                #print(len(self.colors))

    def color_detect_2(self, signals_data_2):
        self.colors = []
        for value in signals_data_2.values():
            if (value[2] == 'Red'):
                self.colors.append((255, 0, 0))
            if (value[2] == 'Blue'):
                self.colors.append((0, 0, 255))
            if (value[2] == 'Green'):
                self.colors.append((0, 250, 0))
                # print('colors')
                # print(len(self.colors))

    #A function to determine the visibility of each signal based on the checkbox value
    def show_hide_1(self, signals_data_1):
        self.hide_signals= []
        for value in signals_data_1.values():
            if(value[4] == True):
                self.hide_signals.append(True)
            else :
                self.hide_signals.append(False)

    def show_hide_2(self, signals_data_1):
        self.hide_signals= []
        for value in signals_data_1.values():
            if(value[4] == True):
                self.hide_signals.append(True)
            else :
                self.hide_signals.append(False)

    def Handle_graph_1(self , signals_data_1 ):
        #self.graphicsView_1 = PlotWidget(self.widget)
        #colors = [(255,0,0),(0,255,0),(0,0,255)]
        self.color_detect_1(signals_data_1)
        self.graphicsView_1.setObjectName("graphicsView_1")
        self.data_lines_1 = []
        
        self.graphicsView_1.setXRange(0, 0.154)
        
        
        #iterate over the values of the dictionary
        self.file_names = []
        for value in signals_data_1.values():
            self.file_names.append( value[5])
            #print(f'file: {self.file_names}')
        #for value in signals_data_1.values():
            
            #self.colors.append(self.color_detect_1(value[2]))
            
        print(f'number in files: {len(self.file_names)}')
        for i,file_name in enumerate(self.file_names):
           #print("i is " )
           #print (i)
           #print(len(self.colors))
           pen = pg.mkPen(color=self.colors[i])
           #pen = pg.mkPen(color=(250 ,0,0))
           df = pd.read_csv(file_name)
        #list_df.append(pd.read_csv(file_name))
           x = df.iloc[:, 0].tolist()
        #self.x = list(range(100))  # 100 time points
        #self.y = [randint(0, 100) for _ in range(100)]  # 100 data points
           y = df.iloc[:, 1].tolist()
           
           data_line = self.graphicsView_1.plot(x, y, pen=pen)
           data_line.x_data = x
           data_line.y_data = y
           self.data_lines_1.append(data_line)
           #print(len(self.data_lines_1))
        self.timer_1 = QtCore.QTimer()
        self.timer_1.setInterval(50)
        self.timer_1.timeout.connect(self.update_plot_data_1)
        self.timer_1.start()
        self.max_range_1()
        self.graphicsView_1.setYRange(-self.max_y, self.max_y)

    def update_plot_data_1(self  ):
        speed_of_signal = 9 / self.number_of_points
        step_in_x = speed_of_signal * self.max_x
        self.end_indx_1+=9
        if(self.end_indx_1>=400 and self.end_indx_1<self.number_of_points):
            self.start_1 = self.start_1 + step_in_x
            self.end_1 = self.end_1 + step_in_x
        if (self.end_indx_1 <= 500 ):
                self.graphicsView_1.setXRange(0, 0.154)
        else:
            if(self.end_indx_1 > 500):
                self.graphicsView_1.setXRange(self.start_1, self.end_1)

        if(self.end_indx_1 == self.number_of_points):
              self.timer_1.stop()
        for i,data_line in enumerate(self.data_lines_1):
            
            
            x_data = data_line.x_data[:self.end_indx_1]
            
            y_data = data_line.y_data[:self.end_indx_1]
            
            data_line.setData(x_data, y_data)
            
            #print(f'flag is {self.flag_1}')
            if (self.flag_1 == True):
              self.color_detect_1(self.signals_data_1)
              data_line.setPen(self.colors[i])
              self.show_hide_1(self.signals_data_1)
              data_line.setVisible(not self.hide_signals[i])

    # graph 2
    def Handle_graph_2(self, signals_data_2):
        # self.graphicsView_2 = PlotWidget(self.widget)
        # colors = [(255,0,0),(0,255,0),(0,0,255)]
        
        self.color_detect_2(signals_data_2)
        self.graphicsView_2.setObjectName("graphicsView_2")
        self.data_lines_2 = []

        self.graphicsView_2.setXRange(0, 0.154)

        # iterate over the values of the dictionary
        self.file_names = []
        for value in signals_data_2.values():
            self.file_names.append(value[5])
            # print(f'file: {self.file_names}')
        # for value in signals_data_1.values():

        # self.colors.append(self.color_detect_2(value[2]))

        print(f'number in files: {len(self.file_names)}')
        for i, file_name in enumerate(self.file_names):
            # print("i is " )
            # print (i)
            # print(len(self.colors))
            pen = pg.mkPen(color=self.colors[i])
            # pen = pg.mkPen(color=(250 ,0,0))
            df = pd.read_csv(file_name)
            # list_df.append(pd.read_csv(file_name))
            x = df.iloc[:, 0].tolist()
            # self.x = list(range(100))  # 100 time points
            # self.y = [randint(0, 100) for _ in range(100)]  # 100 data points
            y = df.iloc[:, 1].tolist()

            data_line = self.graphicsView_2.plot(x, y, pen=pen)
            data_line.x_data = x
            data_line.y_data = y
            self.data_lines_2.append(data_line)
            # print(len(self.data_lines_2))
        self.timer_2 = QtCore.QTimer()
        self.timer_2.setInterval(50)
        self.timer_2.timeout.connect(self.update_plot_data_2)
        self.timer_2.start()
        self.max_range_2()
        self.graphicsView_2.setYRange(-self.max_y, self.max_y)

    def update_plot_data_2(self):
        speed_of_signal = 9 / self.number_of_points
        step_in_x = speed_of_signal * self.max_x
        self.end_indx_2 += 9
        if (self.end_indx_2 >= 400 and self.end_indx_2 < self.number_of_points):
            self.start_2 = self.start_2 + step_in_x
            self.end_2 = self.end_2 + step_in_x
        if (self.end_indx_2 <= 500):
            self.graphicsView_2.setXRange(0, 0.154)
        else:
            if (self.end_indx_2 > 500):
                self.graphicsView_2.setXRange(self.start_2, self.end_2)

        if (self.end_indx_2 == self.number_of_points):
            self.timer_2.stop()
        for i, data_line in enumerate(self.data_lines_2):

            x_data = data_line.x_data[:self.end_indx_2]

            y_data = data_line.y_data[:self.end_indx_2]

            data_line.setData(x_data, y_data)

            # print(f'flag is {self.flag_2}')
            if (self.flag_2 == True):
                self.color_detect_2(self.signals_data_2)
                data_line.setPen(self.colors[i])
                self.show_hide_2(self.signals_data_2)
                data_line.setVisible(not self.hide_signals[i])

    def Handle_btn(self):
        # menu buttons
        self.add_to_graph_1_btn.triggered.connect(self.add_signal_to_graph_1)
        self.add_to_graph_2_btn.triggered.connect(self.add_signal_to_graph_2)
        self.make_pdf_btn.triggered.connect(self.capture_and_create_pdf)
        # graph buttons
        self.graph1_radio_btn.toggled.connect(self.graph1_selected)
        self.graph2_radio_btn.toggled.connect(self.graph2_selected)
        self.link_radio_btn.toggled.connect(self.link_selected)
        self.speed_push_btn.clicked.connect(self.speed_changed)
        self.play_pause_btn.clicked.connect(self.play_pause)
        self.zoom_out_push_btn.clicked.connect(self.zoom_out)
        self.zoom_in_push_btn.clicked.connect(self.zoom_in)
        self.rewind_push_btn.clicked.connect(self.rewind_graph)
        self.clear_push_btn.clicked.connect(self.clear_graph)
        self.snap_shot_btn.clicked.connect(self.save_snap_shot)
        # signal buttons
        self.save_lbl_g1_btn.clicked.connect(self.save_changes_g1)
        self.save_lbl_g2_btn.clicked.connect(self.save_changes_g2)
        self.g_1_signals_combo_box.currentIndexChanged.connect(self.on_combobox_g_1_selection)
        self.g_2_signals_combo_box.currentIndexChanged.connect(self.on_combobox_g_2_selection)

    # A Function  that defines some shortcuts to make the work with our app more easier
    def shortcuts(self):
        # defining shortcuts
        self.sc_export = QShortcut(QKeySequence('Ctrl+E'), self)
        self.sc_g1 = QShortcut(QKeySequence('Ctrl+1'), self)
        self.sc_g2 = QShortcut(QKeySequence('Ctrl+2'), self)
        self.sc_link = QShortcut(QKeySequence('Ctrl+L'), self)
        self.sc_speed = QShortcut(QKeySequence('Ctrl+S'), self)
        self.sc_play = QShortcut(QKeySequence(' '), self)
        self.sc_clear = QShortcut(QKeySequence('Ctrl+C'), self)
        self.sc_zoom_out = QShortcut(QKeySequence('+'), self)
        self.sc_zoom_in = QShortcut(QKeySequence('-'), self)
        self.sc_rewind = QShortcut(QKeySequence('Ctrl+R'), self)

        # activating shortcuts

        self.sc_export.activated.connect(self.capture_and_create_pdf)
        self.sc_g1.activated.connect(self.graph1_selected)
        self.sc_g2.activated.connect(self.graph2_selected)
        self.sc_link.activated.connect(self.link_selected)
        self.sc_speed.activated.connect(self.speed_changed)
        self.sc_play.activated.connect(self.play_pause)
        self.sc_clear.activated.connect(self.clear_graph)
        self.sc_zoom_in.activated.connect(self.zoom_in)
        self.sc_zoom_out.activated.connect(self.zoom_out)
        self.sc_rewind.activated.connect(self.rewind_graph)

    # A function to let the user load the signal file, create another signal element in the dictionary, and send the file to the graph
    def add_signal_to_graph_1(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)",
                                                   options=options)
        if file_path:
            self.count_signals_1 += 1
            file_name = file_path.split("/")[-1]
            self.file_names.append(file_name)
            # print(file_name)
            signal_data = pd.read_csv(file_name)
            # print(signal_data)
            time_column = signal_data.iloc[:, 0]
            values_column = signal_data.iloc[:, 1]
            # Convert the extracted columns to lists
            time_values = time_column.tolist()
            v_values = values_column.tolist()
            if(self.flag_of_speed == False):
                self.max_x = max(time_values)
                self.number_of_points = len(time_values)
                self.flag_of_speed = True
            # print(time_values)
            # print(v_values)
            # print(self.count_signals_!)
            self.signals_data_1[self.count_signals_1] = [time_values, v_values, 'Red', f"{'Signal'} - {self.count_signals_1}",
                                                     False, file_name]
            # print(self.signals_data_1[self.count_signals_1][3])
            self.g_1_signals_combo_box.addItem(f"{'Signal'} - {self.count_signals_1}")
            self.start_flag = False
        self.Handle_graph_1(self.signals_data_1)
        # Update the table with the latest data
        self.loaddata()

    def add_signal_to_graph_2(self):
            options = QFileDialog.Options()
            options |= QFileDialog.ReadOnly
            file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)",
                                                       options=options)
            if file_path:
                self.count_signals_2 += 1
                file_name = file_path.split("/")[-1]
                self.file_names.append(file_name)
                # print(file_name)
                signal_data = pd.read_csv(file_name)
                # print(signal_data)
                time_column = signal_data.iloc[:, 0]
                values_column = signal_data.iloc[:, 1]
                # Convert the extracted columns to lists
                time_values = time_column.tolist()
                v_values = values_column.tolist()
                if(self.flag_of_speed == False):
                    self.max_x = max(time_values)
                    self.number_of_points = len(time_values)
                    self.flag_of_speed = True
                # print(time_values)
                # print(v_values)
                # print(self.count_signals_!)
                self.signals_data_2[self.count_signals_2] = [time_values, v_values, 'Red',
                                                             f"{'Signal'} - {self.count_signals_2}",
                                                             False, file_name]
                self.g_2_signals_combo_box.addItem(f"{'Signal'} - {self.count_signals_2}")
                self.start_flag = False
            self.Handle_graph_2(self.signals_data_2)
            # Update the table with the latest data
            self.loaddata()

    # A function that displays the data of the signal based on which signal has been selected from the comboBox
    def on_combobox_g_1_selection(self):
        self.selected_item_index = self.g_1_signals_combo_box.currentIndex()
        #print(self.selected_item_index)
        self.color_g1_combo_btn.setCurrentText(self.signals_data_1[self.selected_item_index][2])
        
        self.line_edit_g1.setText(self.signals_data_1[self.selected_item_index][3])
        self.hide_g1_check_btn.setChecked(self.signals_data_1[self.selected_item_index][4])

    def on_combobox_g_2_selection(self):
        self.selected_item_index = self.g_2_signals_combo_box.currentIndex()
        # print(self.selected_item_index)
        self.color_g2_combo_btn.setCurrentText(self.signals_data_2[self.selected_item_index][2])

        self.line_edit_g2.setText(self.signals_data_2[self.selected_item_index][3])
        self.hide_g2_check_btn.setChecked(self.signals_data_2[self.selected_item_index][4])

    #A function that update the data of the signal whenever the user change the data and press on save button
    def save_changes_g1(self):

        label_text = self.line_edit_g1.text()
        # Get the selected color from the ComboBox
        selected_color = self.color_g1_combo_btn.currentText()
        checkbox_checked = self.hide_g1_check_btn.isChecked()
        self.signals_data_1[self.selected_item_index][2] = selected_color
        
        self.signals_data_1[self.selected_item_index][3] = label_text
        self.signals_data_1[self.selected_item_index][4] = checkbox_checked
        self.flag_1 = True


    def save_changes_g2(self):

        label_text = self.line_edit_g2.text()
        # Get the selected color from the ComboBox
        selected_color = self.color_g2_combo_btn.currentText()
        checkbox_checked = self.hide_g2_check_btn.isChecked()
        self.signals_data_2[self.selected_item_index][2] = selected_color

        self.signals_data_2[self.selected_item_index][3] = label_text
        self.signals_data_2[self.selected_item_index][4] = checkbox_checked
        self.flag_2 = True


    def capture_and_create_pdf(self):
        # Prompt the user to choose the destination directory and file name
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Save PDF")
        file_dialog.setFileMode(QFileDialog.AnyFile)
        file_dialog.setNameFilter("PDF files (*.pdf)")
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)

        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()

            if selected_files:
                pdf_filename = selected_files[0]

                if not pdf_filename.lower().endswith(".pdf"):
                    # Ensure the file has a .pdf extension
                    pdf_filename += ".pdf"

                # Create a PDF document
                doc = SimpleDocTemplate(pdf_filename, pagesize=letter)

                # Add tables with statistics for all signals in graph 1
                for signal_index, signal_info in self.signals_data_1.items():
                    time_values, signal_values, signal_color, signal_name, __, _ = signal_info
                    mean_value = np.mean(signal_values)
                    std_deviation = np.std(signal_values)
                    duration = time_values[-1] - time_values[0]
                    min_value = np.min(signal_values)
                    max_value = np.max(signal_values)

                    # Add a title for the signal
                    signal_name =f"Graph 1 {signal_info[3]}."
                    self.pdf_content.append(Table([[signal_name]], style=[
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                    ]))

                    # Add statistics to the table
                    table_data = [["Statistic", "Value"]]
                    stat_data = [
                        ["Mean", f"{mean_value:.2f}"],
                        ["Std Deviation", f"{std_deviation:.2f}"],
                        ["Duration", f"{duration:.2f}"],
                        ["Min", f"{min_value:.2f}"],
                        ["Max", f"{max_value:.2f}"],
                    ]
                    table_data.extend(stat_data)

                    # Create the table
                    table = Table(table_data, colWidths=[2 * inch, 2 * inch])
                    table.setStyle(TableStyle([
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)
                    ]))

                    self.pdf_content.append(table)

                # Add tables with statistics for all signals in graph 2

                for signal_index, signal_info in self.signals_data_2.items():
                    time_values, signal_values, signal_color, signal_name, __, _ = signal_info
                    mean_value = np.mean(signal_values)
                    std_deviation = np.std(signal_values)
                    duration = time_values[-1] - time_values[0]
                    min_value = np.min(signal_values)
                    max_value = np.max(signal_values)

                    # Add a title for the signal
                    signal_name = f"Graph 2 {signal_info[3]}."
                    self.pdf_content.append(Table([[signal_name]], style=[
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                    ]))

                    # Add statistics to the table
                    table_data = [["Statistic", "Value"]]
                    stat_data = [
                        ["Mean", f"{mean_value:.2f}"],
                        ["Std Deviation", f"{std_deviation:.2f}"],
                        ["Duration", f"{duration:.2f}"],
                        ["Min", f"{min_value:.2f}"],
                        ["Max", f"{max_value:.2f}"],
                    ]
                    table_data.extend(stat_data)

                    # Create the table
                    table = Table(table_data, colWidths=[2 * inch, 2 * inch])
                    table.setStyle(TableStyle([
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)
                    ]))

                    self.pdf_content.append(table)

                # Build and save the PDF document
                doc.build(self.pdf_content)

                # Delete the temporary snapshot image
                for i in range(self.snapshot_counter):
                    self.snapshot_path = f"temp_snapshot_{i}.png"
                    os.remove(self.snapshot_path)
                self.snapshot_counter = 0
                # Clear PDF file
                self.pdf_content = []
                self.title_pdf()
                print(f'PDF with snapshots and statistics saved as {pdf_filename}')

    def save_snap_shot(self):
        if (self.graph_1_active == True and self.graph_2_active == False):

            title = "Graph 1"
            self.pdf_content.append(Table([[title]], style=[
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ]))
            # Calculate the size of the snapshot image
            plot_widget_image = QImage(self.graphicsView_1.size(), QImage.Format_ARGB32)
            plot_widget_image.fill(Qt.transparent)
            painter = QPainter(plot_widget_image)

            # Ensure that the y-axis is visible
            self.graphicsView_1.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
            self.graphicsView_1.render(painter)

            painter.end()

            # Save the snapshot as a temporary image
            # Create the snapshot path with an incrementing number
            self.snapshot_path = f"temp_snapshot_{self.snapshot_counter}.png"
            plot_widget_image.save(self.snapshot_path)

            print(self.snapshot_path)

            # Add the snapshot image to the PDF
            im = Image(self.snapshot_path, width=6 * inch, height=4 * inch)
            self.pdf_content.append(im)
            self.pdf_content.append(Spacer(1, 0.2 * inch))

            # Increment the counter for the next snapshot
            self.snapshot_counter += 1
        elif (self.graph_1_active == False and self.graph_2_active == True):
            title = "Graph 2"
            self.pdf_content.append(Table([[title]], style=[
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ]))
            # Calculate the size of the snapshot image
            plot_widget_image = QImage(self.graphicsView_2.size(), QImage.Format_ARGB32)
            plot_widget_image.fill(Qt.transparent)
            painter = QPainter(plot_widget_image)

            # Ensure that the y-axis is visible
            self.graphicsView_2.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
            self.graphicsView_2.render(painter)

            painter.end()

            # Save the snapshot as a temporary image
            # Create the snapshot path with an incrementing number
            self.snapshot_path = f"temp_snapshot_{self.snapshot_counter}.png"
            plot_widget_image.save(self.snapshot_path)

            print(self.snapshot_path)

            # Add the snapshot image to the PDF
            im = Image(self.snapshot_path, width=6 * inch, height=4 * inch)
            self.pdf_content.append(im)
            self.pdf_content.append(Spacer(1, 0.2 * inch))

            # Increment the counter for the next snapshot
            self.snapshot_counter += 1
        elif (self.graph_1_active == True and self.graph_2_active == True):
            title = "Graph 1 & Graph 2"
            self.pdf_content.append(Table([[title]], style=[
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ]))
            # graph 1
            # Calculate the size of the snapshot image
            plot_widget_image = QImage(self.graphicsView_1.size(), QImage.Format_ARGB32)
            plot_widget_image.fill(Qt.transparent)
            painter = QPainter(plot_widget_image)

            # Ensure that the y-axis is visible
            self.graphicsView_1.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
            self.graphicsView_1.render(painter)

            painter.end()

            # Save the snapshot as a temporary image
            # Create the snapshot path with an incrementing number
            self.snapshot_path = f"temp_snapshot_{self.snapshot_counter}.png"
            plot_widget_image.save(self.snapshot_path)

            print(self.snapshot_path)

            # Add the snapshot image to the PDF
            im = Image(self.snapshot_path, width=6 * inch, height=4 * inch)
            self.pdf_content.append(im)
            self.pdf_content.append(Spacer(1, 0.2 * inch))

            # Increment the counter for the next snapshot
            self.snapshot_counter += 1
            # graph 2
            # Calculate the size of the snapshot image
            plot_widget_image = QImage(self.graphicsView_2.size(), QImage.Format_ARGB32)
            plot_widget_image.fill(Qt.transparent)
            painter = QPainter(plot_widget_image)

            # Ensure that the y-axis is visible
            self.graphicsView_2.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
            self.graphicsView_2.render(painter)

            painter.end()

            # Save the snapshot as a temporary image
            # Create the snapshot path with an incrementing number
            self.snapshot_path = f"temp_snapshot_{self.snapshot_counter}.png"
            plot_widget_image.save(self.snapshot_path)

            print(self.snapshot_path)

            # Add the snapshot image to the PDF
            im = Image(self.snapshot_path, width=6 * inch, height=4 * inch)
            self.pdf_content.append(im)
            self.pdf_content.append(Spacer(1, 0.2 * inch))

            # Increment the counter for the next snapshot
            self.snapshot_counter += 1

    def title_pdf(self):
        # Add a title for the PDF
        title = "Signal PDF Report"
        self.pdf_content.append(Table([[title]], style=[
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))

    def graph1_selected(self ):

        self.graph_1_active = True
        self.graph_2_active = False

    def graph2_selected(self):

        self.graph_1_active = False
        self.graph_2_active = True

    def link_selected(self):

        self.graph_1_active = True
        self.graph_2_active = True

    def speed_changed(self):

        if (self.current_speed_index == 3):
            self.speed_push_btn.setText(self.speeds[0])
            self.current_speed_index = 0
        else :    
            self.current_speed_index = self.current_speed_index + 1
            self.speed_push_btn.setText(self.speeds[self.current_speed_index])

        # A function that triggers between play and pause to control the flow of signals on graph

    def play_pause(self):

        if (self.graph_1_active == True and self.graph_2_active==False ):
            self.is_playing_g_1 = not self.is_playing_g_1
            if self.is_playing_g_1:
                self.timer_1.start()
            # print('start')

            else:
                self.timer_1.stop()
            # print('stop')
        elif (self.graph_1_active == False and self.graph_2_active==True):
            self.is_playing_g_2 = not self.is_playing_g_2
            if self.is_playing_g_2:
                self.timer_2.start()
            # print('start')

            else:
                self.timer_2.stop()
            # print('stop')
        elif (self.graph_1_active == True and self.graph_2_active==True):
           # graph 1
            self.is_playing_g_1 = not self.is_playing_g_1
            if self.is_playing_g_1:
                self.timer_1.start()
            else:
                self.timer_1.stop()
            # graph 2
            self.is_playing_g_2 = not self.is_playing_g_2
            if self.is_playing_g_2:
                self.timer_2.start()
            else:
                self.timer_2.stop()

    def clear_graph(self):
        if (self.graph_1_active == True and self.graph_2_active==False ):
            self.timer_1.stop()  # Stop the timer
            self.graphicsView_1.clear()  # Clear the graph

            # Reset start, end, and end_indx
            self.end_indx_1 = 50
            self.start_1 = 0
            self.end_1 = 0.154
        elif (self.graph_1_active == False and self.graph_2_active==True):
            self.timer_2.stop()  # Stop the timer
            self.graphicsView_2.clear()  # Clear the graph

            # Reset start, end, and end_indx
            self.end_indx_2 = 50
            self.start_2 = 0
            self.end_2 = 0.154
        elif (self.graph_1_active == True and self.graph_2_active==True):
           # graph 1
           self.timer_1.stop()  # Stop the timer
           self.graphicsView_1.clear()  # Clear the graph

           # Reset start, end, and end_indx
           self.end_indx_1 = 50
           self.start_1 = 0
           self.end_1 = 0.154

           # graph 2
           self.timer_2.stop()  # Stop the timer
           self.graphicsView_2.clear()  # Clear the graph

           # Reset start, end, and end_indx
           self.end_indx_2 = 50
           self.start_2 = 0
           self.end_2 = 0.154

    def zoom_out(self):
        if (self.graph_1_active == True and self.graph_2_active==False ):
            # Get the current visible x and y ranges
            x_min, x_max = self.graphicsView_1.getViewBox().viewRange()[0]
            y_min, y_max = self.graphicsView_1.getViewBox().viewRange()[1]

            # Calculate the new visible x and y ranges (zoom in)
            new_x_min = x_min * 0.5
            new_x_max = x_max * 0.5
            new_y_min = y_min * 0.5
            new_y_max = y_max * 0.5

            # Set the new visible x and y ranges
            self.graphicsView_1.getViewBox().setRange(xRange=[new_x_min, new_x_max], yRange=[new_y_min, new_y_max])

        elif (self.graph_1_active == False and self.graph_2_active==True):
            # Get the current visible x and y ranges
            x_min, x_max = self.graphicsView_2.getViewBox().viewRange()[0]
            y_min, y_max = self.graphicsView_2.getViewBox().viewRange()[1]

            # Calculate the new visible x and y ranges (zoom in)
            new_x_min = x_min * 0.5
            new_x_max = x_max * 0.5
            new_y_min = y_min * 0.5
            new_y_max = y_max * 0.5

            # Set the new visible x and y ranges
            self.graphicsView_2.getViewBox().setRange(xRange=[new_x_min, new_x_max], yRange=[new_y_min, new_y_max])
        elif (self.graph_1_active == True and self.graph_2_active==True):
           # graph 1

           # Get the current visible x and y ranges
           x_min, x_max = self.graphicsView_1.getViewBox().viewRange()[0]
           y_min, y_max = self.graphicsView_1.getViewBox().viewRange()[1]

           # Calculate the new visible x and y ranges (zoom in)
           new_x_min = x_min * 0.5
           new_x_max = x_max * 0.5
           new_y_min = y_min * 0.5
           new_y_max = y_max * 0.5

           # Set the new visible x and y ranges
           self.graphicsView_1.getViewBox().setRange(xRange=[new_x_min, new_x_max], yRange=[new_y_min, new_y_max])
            # graph 2

           # Get the current visible x and y ranges
           x_min, x_max = self.graphicsView_2.getViewBox().viewRange()[0]
           y_min, y_max = self.graphicsView_2.getViewBox().viewRange()[1]

           # Calculate the new visible x and y ranges (zoom in)
           new_x_min = x_min * 0.5
           new_x_max = x_max * 0.5
           new_y_min = y_min * 0.5
           new_y_max = y_max * 0.5

           # Set the new visible x and y ranges
           self.graphicsView_2.getViewBox().setRange(xRange=[new_x_min, new_x_max], yRange=[new_y_min, new_y_max])

    def zoom_in(self):

        if (self.graph_1_active == True and self.graph_2_active == False):
            # Get the current visible x and y ranges
            x_min, x_max = self.graphicsView_1.getViewBox().viewRange()[0]
            y_min, y_max = self.graphicsView_1.getViewBox().viewRange()[1]

            # Calculate the new visible x and y ranges (zoom in)
            new_x_min = x_min * 1.3
            new_x_max = x_max * 1.3
            new_y_min = y_min * 1.3
            new_y_max = y_max * 1.3

            # Set the new visible x and y ranges
            self.graphicsView_1.getViewBox().setRange(xRange=[new_x_min, new_x_max], yRange=[new_y_min, new_y_max])

        elif (self.graph_1_active == False and self.graph_2_active == True):
            # Get the current visible x and y ranges
            x_min, x_max = self.graphicsView_2.getViewBox().viewRange()[0]
            y_min, y_max = self.graphicsView_2.getViewBox().viewRange()[1]

            # Calculate the new visible x and y ranges (zoom in)
            new_x_min = x_min * 1.3
            new_x_max = x_max * 1.3
            new_y_min = y_min * 1.3
            new_y_max = y_max * 1.3

            # Set the new visible x and y ranges
            self.graphicsView_2.getViewBox().setRange(xRange=[new_x_min, new_x_max], yRange=[new_y_min, new_y_max])
        elif (self.graph_1_active == True and self.graph_2_active == True):
            # graph 1
            # Get the current visible x and y ranges
            x_min, x_max = self.graphicsView_1.getViewBox().viewRange()[0]
            y_min, y_max = self.graphicsView_1.getViewBox().viewRange()[1]

            # Calculate the new visible x and y ranges (zoom in)
            new_x_min = x_min * 1.3
            new_x_max = x_max * 1.3
            new_y_min = y_min * 1.3
            new_y_max = y_max * 1.3

            # Set the new visible x and y ranges
            self.graphicsView_1.getViewBox().setRange(xRange=[new_x_min, new_x_max], yRange=[new_y_min, new_y_max])
            # graph 2
            # Get the current visible x and y ranges
            x_min, x_max = self.graphicsView_2.getViewBox().viewRange()[0]
            y_min, y_max = self.graphicsView_2.getViewBox().viewRange()[1]

            # Calculate the new visible x and y ranges (zoom in)
            new_x_min = x_min * 1.3
            new_x_max = x_max * 1.3
            new_y_min = y_min * 1.3
            new_y_max = y_max * 1.3

            # Set the new visible x and y ranges
            self.graphicsView_2.getViewBox().setRange(xRange=[new_x_min, new_x_max], yRange=[new_y_min, new_y_max])

    def rewind_graph(self):
        if (self.graph_1_active == True and self.graph_2_active==False ):
            # Clear Graph
            self.clear_graph()

            # Replot all the signals
            self.Handle_graph_1(self.signals_data_1)
        elif (self.graph_1_active == False and self.graph_2_active==True):
            # Clear Graph
            self.clear_graph()

            # Replot all the signals
            self.Handle_graph_2(self.signals_data_2)
        elif (self.graph_1_active == True and self.graph_2_active==True):
           # graph 1
           # Clear Graph
           self.clear_graph()

           # Replot all the signals
           self.Handle_graph_1(self.signals_data_1)

           # graph 2

           # Replot all the signals
           self.Handle_graph_2(self.signals_data_2)

    def loaddata(self):
        # Clear the table
        self.tableWidget.clear()

        # Get the number of signals and statistics
        num_signals = len(self.signals_data_1) + len(self.signals_data_2)
        num_stats = 5  # There are 5 statistics for each signal

        # Set the table row count based on the number of signals and statistics
        self.tableWidget.setRowCount(num_signals + 1)  # Signals rows (+1 for the statistic names)
        self.tableWidget.setColumnCount(num_stats + 1)  # Statistics columns (+1 for signal labels)

        # Define a list of statistic names
        statistic_names = ["Statistic", "Mean", "Std", "Duration", "Min", "Max"]

        # Set the table headers for statistics and signal labels
        for col, header in enumerate(statistic_names):
            self.tableWidget.setItem(0, col, QTableWidgetItem(header))

        # Loop through each signal in graph 1 and populate the table with statistics
        for signal_index, signal_info in self.signals_data_1.items():
            time_values, signal_values, signal_color, signal_name, __, _ = signal_info

            # Calculate statistics for the current signal
            mean_value = np.mean(signal_values)
            std_deviation = np.std(signal_values)
            duration = time_values[-1] - time_values[0]
            min_value = np.min(signal_values)
            max_value = np.max(signal_values)

            # Set the signal label in the row header
            signal_name = f"Graph 1 {signal_info[3]}"
            self.tableWidget.setItem(signal_index, 0, QTableWidgetItem(signal_name))

            # Fill the table with statistics values based on the statistic name
            for col, stat_name in enumerate(statistic_names[1:]):  # Skip "Statistic" for each statistic
                # Fill the table with statistics values for the current signal
                if stat_name == "Mean":
                    self.tableWidget.setItem(signal_index, col + 1, QTableWidgetItem(f"{mean_value:.2f}"))
                elif stat_name == "Std":
                    self.tableWidget.setItem(signal_index, col + 1, QTableWidgetItem(f"{std_deviation:.2f}"))
                elif stat_name == "Duration":
                    self.tableWidget.setItem(signal_index, col + 1, QTableWidgetItem(f"{duration:.2f}"))
                elif stat_name == "Min":
                    self.tableWidget.setItem(signal_index, col + 1, QTableWidgetItem(f"{min_value:.2f}"))
                elif stat_name == "Max":
                    self.tableWidget.setItem(signal_index, col + 1, QTableWidgetItem(f"{max_value:.2f}"))

        # Loop through each signal in graph 2 and populate the table with statistics
        for signal_index, signal_info in self.signals_data_2.items():
            time_values, signal_values, signal_color, signal_name, __, _ = signal_info
            signal_index = signal_index + len(self.signals_data_1)
            # Calculate statistics for the current signal
            mean_value = np.mean(signal_values)
            std_deviation = np.std(signal_values)
            duration = time_values[-1] - time_values[0]
            min_value = np.min(signal_values)
            max_value = np.max(signal_values)

            # Set the signal label in the row header
            signal_name = f"Graph 2 {signal_info[3]}"
            self.tableWidget.setItem(signal_index, 0, QTableWidgetItem(signal_name))

            # Fill the table with statistics values based on the statistic name
            for col, stat_name in enumerate(statistic_names[1:]):  # Skip "Statistic" for each statistic
                # Fill the table with statistics values for the current signal
                if stat_name == "Mean":
                    self.tableWidget.setItem(signal_index, col + 1, QTableWidgetItem(f"{mean_value:.2f}"))
                elif stat_name == "Std":
                    self.tableWidget.setItem(signal_index, col + 1, QTableWidgetItem(f"{std_deviation:.2f}"))
                elif stat_name == "Duration":
                    self.tableWidget.setItem(signal_index, col + 1, QTableWidgetItem(f"{duration:.2f}"))
                elif stat_name == "Min":
                    self.tableWidget.setItem(signal_index, col + 1, QTableWidgetItem(f"{min_value:.2f}"))
                elif stat_name == "Max":
                    self.tableWidget.setItem(signal_index, col + 1, QTableWidgetItem(f"{max_value:.2f}"))


def main():  # method to start app
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()  # infinte Loop


if __name__ == '__main__':
    main()

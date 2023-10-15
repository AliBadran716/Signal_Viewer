from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
import pyqtgraph as pg
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pyqtgraph import PlotWidget, plot
from PyQt5.QtWidgets import QGraphicsScene
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Image
from reportlab.lib import colors
from reportlab.platypus import KeepTogether
from reportlab.lib.pagesizes import inch
import os
import sys
from os import path


FORM_CLASS, _ = loadUiType(path.join(path.dirname(__file__), "main.ui"))  # connects the Ui file with the Python file

class MainApp(QMainWindow, FORM_CLASS):  # go to the main window in the form_class file

    def __init__(self, parent=None):  # constructor to intiate the main window  in the design
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setGeometry(0, 0, 1300, 700)  # Initialization for the UI
        self.center_on_screen()
        self.handle_btn()
        self.shortcuts()
        self.graphicsView_1.setBackground('w')
        self.graphicsView_2.setBackground('w')
        # A dict to save the data of all signals as pairs of keys and values, the key is a counter for the signals 
        # The value is a list that contains the data of each signal in the form of :
        # [[x_values], [y_values], [color_of signal], label_of_signal, is_hide, file_name]
        self.signals_data_1 = {}
        self.signals_data_2 = {}
        self.file_names_1 = []  # A list to contain the file names being uploaded
        self.file_names_2 = []
        # A list to contain the colors of the signals
        self.graphicsView_1.setLabel('bottom', 'time')
        self.graphicsView_2.setLabel('bottom', 'time')
        # Initialization of the ranges of the sliders
        self.move_y_slider.setMinimum(-50) 
        self.move_y_slider.setMaximum(50)   
        self.move_y_slider.setSliderPosition(0)
        self.move_x_slider.setMinimum(-50) 
        self.move_x_slider.setMaximum(50)   
        self.move_x_slider.setSliderPosition(0)
        self.graph_1_active = True  # Setting graph 1 active initially
        self.graph_2_active = False
        self.is_playing_g_1 = True
        self.is_playing_g_2 = True
        # Initialization of the min and max values of x-axis and y-axis
        self.first_element_of_time = 0
        self.max_y_1 = 0
        self.max_y_2 = 0
        self.max_x_1 = 0
        self.max_x_2 = 0
        self.count_signals_1 = 0  # Setting the counter of the signals initially by zero
        self.count_signals_2 = 0
        self.snapshot_counter = 0
        self.zoom_count_graph1 = 0  # Initialize zoom count for graph 1
        self.zoom_count_graph2 = 0  # Initialize zoom count for graph 2
        self.end_indx_1 = 50  # Tracks the last index plotted from the signal
        self.end_indx_2 = 50
        self.start_1 = 0  # Sets the start of the x range
        self.start_2 = 0
        self.end_1 = 616 * self.first_element_of_time  # Sets the end of the x range
        self.end_2 = 616 * self.first_element_of_time
        self.load_data()
        self.show_signals = []
        self.number_of_points_1 = 0 
        self.number_of_points_2 = 0
        self.start_flag_1 = False  # Determines whether a new signal ia added or not
        self.start_flag_2 = False
        self.terminal_flag_1 = False  # Determines the max value at which the plotting will terminate
        self.terminal_flag_2 = False
        # Hanlding the pdf data
        self.pdf_content = []
        self.title_pdf()
        self.snapshot_path = ''

    # A function that centers the screen
    def center_on_screen(self):
        # Calculate the center coordinates for a 1920x1080 screen
        screen_width = 1920
        screen_height = 1080
        window_width = self.frameGeometry().width()
        window_height = self.frameGeometry().height()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        # Set the window's position to the center
        self.move(x, y)

    # A function that connects the ui elements to function to handle them
    def handle_btn(self):
        # menu buttons
        self.add_to_graph_1_btn.triggered.connect(self.add_signal_to_graph_1)
        self.add_to_graph_2_btn.triggered.connect(self.add_signal_to_graph_2)
        self.make_pdf_btn.triggered.connect(self.capture_and_create_pdf)
        # graph buttons
        self.move_y_slider.valueChanged.connect(self.onSliderValueChanged_y)
        self.move_x_slider.valueChanged.connect(self.onSliderValueChanged_x)
        self.graph1_radio_btn.toggled.connect(self.graph1_selected)
        self.graph2_radio_btn.toggled.connect(self.graph2_selected)
        self.link_radio_btn.toggled.connect(self.link_selected)
        self.speed_selection.currentIndexChanged.connect(self.on_combobox_speed_selection)
        self.play_pause_btn.clicked.connect(self.play_pause)
        self.zoom_out_push_btn.clicked.connect(self.zoom_out)
        self.zoom_in_push_btn.clicked.connect(self.zoom_in)
        self.rewind_push_btn.clicked.connect(self.rewind_graph)
        self.clear_push_btn.clicked.connect(self.clear_graph)
        self.snap_shot_btn.clicked.connect(self.save_snap_shot)
        self.g_1_signals_combo_box.currentIndexChanged.connect(self.on_combobox_g_1_selection)
        self.g_2_signals_combo_box.currentIndexChanged.connect(self.on_combobox_g_2_selection)
        self.delete_g1_btn.clicked.connect(self.delete_signal_g_1)
        self.delete_g2_btn.clicked.connect(self.delete_signal_g_2)
        self.save_lbl_g1_btn.clicked.connect(self.save_changes_g1)
        self.save_lbl_g2_btn.clicked.connect(self.save_changes_g2)
        self.show_g1_check_btn.stateChanged.connect(self.show_hide_signal_g_1)
        self.show_g2_check_btn.stateChanged.connect(self.show_hide_signal_g_2)
        self.move_g1_btn.clicked.connect(self.move_signal_g_1)
        self.move_g2_btn.clicked.connect(self.move_signal_g_2)


    # A Function  that defines some shortcuts to make the work with our app more easier
    def shortcuts(self):
        # defining shortcuts
        self.sc_add_to_g_1 = QShortcut(QKeySequence('Ctrl+SHIFT+1'), self)
        self.sc_add_to_g_2 = QShortcut(QKeySequence('Ctrl+SHIFT+2'), self)
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
        self.sc_add_to_g_1.activated.connect(self.add_signal_to_graph_1)
        self.sc_add_to_g_2.activated.connect(self.add_signal_to_graph_2)
        self.sc_export.activated.connect(self.capture_and_create_pdf)
        self.sc_g1.activated.connect(self.graph1_selected)
        self.sc_g2.activated.connect(self.graph2_selected)
        self.sc_link.activated.connect(self.link_selected)
        self.sc_speed.activated.connect(self.on_combobox_speed_selection)
        self.sc_play.activated.connect(self.play_pause)
        self.sc_clear.activated.connect(self.clear_graph)
        self.sc_zoom_in.activated.connect(self.zoom_in)
        self.sc_zoom_out.activated.connect(self.zoom_out)
        self.sc_rewind.activated.connect(self.rewind_graph)
        

    # A function that detects the max y-value of all the signals in graph 1 
    def max_range_1 (self):
        for value in self.signals_data_1.values():
            for search in value[1]:
                if(search > self.max_y_1):
                  self.max_y_1 = search

    # A function that detects the max y-value of all the signals in graph 2
    def max_range_2 (self):
        for value in self.signals_data_2.values():
            for search in value[1]:
               if(search > self.max_y_2):
                  self.max_y_2 = search

    # A function that detects the colors of all signals in graph 1
    def color_detect_1(self , signals_data_1):
        self.colors = []
        for value in signals_data_1.values():
            if(value[2] == 'Red'):
                self.colors.append((255 , 0 , 0))
            if (value[2] == 'Blue'):
                self.colors.append( (0 , 0, 255)) 
            if (value[2] == 'Green'):
                self.colors.append((0 , 250 , 0))       
              
    # A function that detects the colors of all signals in graph 2
    def color_detect_2(self, signals_data_2):
        self.colors = []
        for value in signals_data_2.values():
            if (value[2] == 'Red'):
                self.colors.append((255, 0, 0))
            if (value[2] == 'Blue'):
                self.colors.append((0, 0, 255))
            if (value[2] == 'Green'):
                self.colors.append((0, 250, 0))
              

    # A function to determine the visibility of each signal based on the checkbox value in graph 1
    def show_hide_1(self, signals_data_1):
        self.show_signals= []
        for value in signals_data_1.values():
            if(value[4] == True):
                self.show_signals.append(True)
            else :
                self.show_signals.append(False)

    # A function to determine the visibility of each signal based on the checkbox value in graph 1
    def show_hide_2(self, signals_data_1):
        self.show_signals= []
        for value in signals_data_1.values():
            if(value[4] == True):
                self.show_signals.append(True)
            else :
                self.show_signals.append(False)

    # A funbction that initilaizes graph 1 
    def handle_graph_1(self , signals_data_1 ):
        self.color_detect_1(signals_data_1)
        self.graphicsView_1.setObjectName("graphicsView_1")
        self.data_lines_1 = []
        self.file_names_1 = []
        self.graphicsView_1.setXRange(0, 616 * self.first_element_of_time)
        for value in signals_data_1.values():
            self.file_names_1.append( value[5]) 
        for i,file_name in enumerate(self.file_names_1):
           pen = pg.mkPen(color=self.colors[i])
           df = pd.read_csv(file_name)
           x = df.iloc[:, 0].tolist()
           y = df.iloc[:, 1].tolist()
           data_line = self.graphicsView_1.plot(x, y, pen=pen)
           data_line.x_data = x
           data_line.y_data = y
           self.data_lines_1.append(data_line)
        if not self.signals_data_1:
            return
        self.end_1 = 616 * self.first_element_of_time # Sets the end of the x range
       
        self.timer_1 = QtCore.QTimer()
        self.timer_1.setInterval(50)
        self.timer_1.timeout.connect(self.update_plot_data_1)
        self.timer_1.start()
        self.max_range_1()
        self.graphicsView_1.setYRange(-self.max_y_1, self.max_y_1)

    # A function that updates the data being plotted on graph 1
    def update_plot_data_1(self  ):
        step_in_x = 9 * self.first_element_of_time
        self.end_indx_1+=9
        if(self.end_indx_1>=616 and self.end_indx_1<self.number_of_points_1):
            self.start_1 = self.start_1 + step_in_x
            
            self.end_1 = self.end_1 + step_in_x
            
        if (self.end_indx_1 <= 616 ):
                self.graphicsView_1.setXRange(0, 616 * self.first_element_of_time)
        else:
            if(self.end_indx_1 > 616):
                self.graphicsView_1.setXRange(self.start_1, self.end_1)
        if(self.end_indx_1 >= self.number_of_points_1):
              self.timer_1.stop()
        for i,data_line in enumerate(self.data_lines_1):
            if(self.start_flag_1 == False and i > 0):
                    graph_1_act = self.graph_1_active
                    graph_2_act = self.graph_2_active
                    self.graph_1_active = True
                    self.graph_2_active = False
                    self.clear_graph()
                    self.handle_graph_1(self.signals_data_1)
                    self.start_flag_1 = True
                    self.graph_1_active = graph_1_act
                    self.graph_2_active = graph_2_act
            else:
                x_data = data_line.x_data[:self.end_indx_1]
                y_data = data_line.y_data[:self.end_indx_1]
                data_line.setData(x_data, y_data)
            
            self.color_detect_1(self.signals_data_1)
            data_line.setPen(self.colors[i])
            self.show_hide_1(self.signals_data_1)
            data_line.setVisible(self.show_signals[i])

     # A funbction that initilaizes graph 2
    def handle_graph_2(self, signals_data_2):
        self.color_detect_2(signals_data_2)
        self.graphicsView_2.setObjectName("graphicsView_2")
        self.data_lines_2 = []
        self.file_names_2 = []
        self.graphicsView_2.setXRange(0, 616 * self.first_element_of_time)

        for value in signals_data_2.values():
            self.file_names_2.append(value[5])

        for i, file_name in enumerate(self.file_names_2):
            pen = pg.mkPen(color=self.colors[i])
            df = pd.read_csv(file_name)
            x = df.iloc[:, 0].tolist()
            y = df.iloc[:, 1].tolist()
            data_line = self.graphicsView_2.plot(x, y, pen=pen)
            data_line.x_data = x
            data_line.y_data = y
            self.data_lines_2.append(data_line)

        if not self.signals_data_2:
            return
        self.end_2 = 616 * self.first_element_of_time
        self.timer_2 = QtCore.QTimer()
        self.timer_2.setInterval(50)
        self.timer_2.timeout.connect(self.update_plot_data_2)
        self.timer_2.start()
        self.max_range_2()
        self.graphicsView_2.setYRange(-self.max_y_2, self.max_y_2)

    # A function that updates the data being plotted on graph 2
    def update_plot_data_2(self):
        step_in_x = 9 * self.first_element_of_time
        
        self.end_indx_2 += 9
        if (self.end_indx_2 >= 616 and self.end_indx_2 < self.number_of_points_2):
            self.start_2 = self.start_2 + step_in_x
            self.end_2 = self.end_2 + step_in_x
            
        if (self.end_indx_2 <= 616):
            self.graphicsView_2.setXRange(0, 616 * self.first_element_of_time)
        else:
            if (self.end_indx_2 > 616):
                self.graphicsView_2.setXRange(self.start_2, self.end_2)
        
        if (self.end_indx_2 >= self.number_of_points_2):
            self.timer_2.stop()
            current_g_1 = self.graph_1_active
            current_g_2 = self.graph_2_active
        for i, data_line in enumerate(self.data_lines_2):
            if(self.start_flag_2 == False and i > 0):
                    graph_1_act = self.graph_1_active
                    graph_2_act = self.graph_2_active
                    self.graph_1_active = False
                    self.graph_2_active = True
                    self.clear_graph()
                    self.handle_graph_2(self.signals_data_2)
                    self.start_flag_2 = True
                    self.graph_1_active = graph_1_act
                    self.graph_2_active = graph_2_act
            else:
                x_data = data_line.x_data[:self.end_indx_2]
                y_data = data_line.y_data[:self.end_indx_2]
                data_line.setData(x_data, y_data)

           
            self.color_detect_2(self.signals_data_2)
            data_line.setPen(self.colors[i])
            self.show_hide_2(self.signals_data_2)
            data_line.setVisible(self.show_signals[i])

    # A function to let the user load the signal file, create another signal element in the dictionary, and send the file to the graph
    def add_signal_to_graph_1(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)",
                                                   options=options)
        if file_path:
            self.count_signals_1 += 1
            file_name = file_path.split("/")[-1]
            self.file_names_1.append(file_name)
            signal_data = pd.read_csv(file_name)
            time_column = signal_data.iloc[:, 0]
            values_column = signal_data.iloc[:, 1]
            time_values = time_column.tolist()
            v_values = values_column.tolist()
            self.first_element_of_time = time_values[1]-time_values[0] 
            

            if(self.terminal_flag_1 == False):
                self.max_x_1 = max(time_values)
                self.number_of_points_1 = len(time_values)
                self.terminal_flag_1 = True
            # Making a new item in the dictionary, the new signal is given a key, and the values is given according to its data
            self.signals_data_1[self.count_signals_1] = [time_values, v_values, 'Red', f"{'Signal'} - {self.count_signals_1}",
                                                     True, file_name]
            self.g_1_signals_combo_box.addItem(f"{'Signal'} - {self.count_signals_1}")
            self.start_flag_1 = False
        self.handle_graph_1(self.signals_data_1)
        # Update the table with the latest data
        self.load_data()

    # A function to let the user load the signal file, create another signal element in the dictionary, and send the file to the graph
    def add_signal_to_graph_2(self):
            options = QFileDialog.Options()
            options |= QFileDialog.ReadOnly
            file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "","CSV Files (*.csv);;All Files (*)",
                                                       options=options)
            if file_path:
                self.count_signals_2 += 1
                file_name = file_path.split("/")[-1]
                self.file_names_2.append(file_name)
                signal_data = pd.read_csv(file_name)
                time_column = signal_data.iloc[:, 0]
                values_column = signal_data.iloc[:, 1]
                time_values = time_column.tolist()
                v_values = values_column.tolist()
                self.first_element_of_time = time_values[1]-time_values[0] 

                if(self.terminal_flag_2 == False):
                    self.max_x_2 = max(time_values)
                    self.number_of_points_2 = len(time_values)
                    self.terminal_flag_2 = True
                self.signals_data_2[self.count_signals_2] = [time_values, v_values, 'Red',
                                                             f"{'Signal'} - {self.count_signals_2}",
                                                             True, file_name]
                self.g_2_signals_combo_box.addItem(f"{'Signal'} - {self.count_signals_2}")
                self.start_flag_2 = False
            self.handle_graph_2(self.signals_data_2)
            self.load_data()


    # A function that displays the data of the signal based on which signal has been selected from the comboBox in graph 1
    def on_combobox_g_1_selection(self):
        selected_item_index = self.g_1_signals_combo_box.currentIndex()
        if not self.signals_data_1 or self.g_1_signals_combo_box.currentIndex() <= 0:
            self.color_g1_combo_btn.setCurrentIndex(selected_item_index)
            self.line_edit_g1.clear()
            self.show_g1_check_btn.setChecked(False)
        else:
            self.color_g1_combo_btn.setCurrentText(self.signals_data_1[selected_item_index][2])
            self.line_edit_g1.setText(self.signals_data_1[selected_item_index][3])
            self.show_g1_check_btn.setChecked(self.signals_data_1[selected_item_index][4])


    # A function that displays the data of the signal based on which signal has been selected from the comboBox in graph 2
    def on_combobox_g_2_selection(self):
        selected_item_index = self.g_2_signals_combo_box.currentIndex()
        if not self.signals_data_2 or self.g_2_signals_combo_box.currentIndex() <= 0:
            self.color_g2_combo_btn.setCurrentIndex(selected_item_index)
            self.line_edit_g2.clear()
            self.show_g2_check_btn.setChecked(False)
        else:
            self.color_g2_combo_btn.setCurrentText(self.signals_data_2[selected_item_index][2])
            self.line_edit_g2.setText(self.signals_data_2[selected_item_index][3])
            self.show_g2_check_btn.setChecked(self.signals_data_2[selected_item_index][4])

    # A function that determines whether to show the signal of hide it, based on the the checkbox value in graph 1
    def show_hide_signal_g_1(self):
        if not self.signals_data_1 or self.g_1_signals_combo_box.currentIndex() <= 0:
            return
        selected_item_index = self.g_1_signals_combo_box.currentIndex()
        checkbox_checked = self.show_g1_check_btn.isChecked()
        self.signals_data_1[selected_item_index][4] = checkbox_checked
       

    # A function that determines whether to show the signal of hide it, based on the the checkbox value in graph 2
    def show_hide_signal_g_2(self):
        if not self.signals_data_2 or self.g_2_signals_combo_box.currentIndex() <= 0:
            return
        selected_item_index = self.g_2_signals_combo_box.currentIndex()
        checkbox_checked = self.show_g2_check_btn.isChecked()
        self.signals_data_2[selected_item_index][4] = checkbox_checked
        

    # A function that updates the data of the signal whenever the user change the data and press on save button in graph 1
    def save_changes_g1(self):
        if not self.signals_data_1:
            return
        selected_item_index = self.g_1_signals_combo_box.currentIndex()
        label_text = self.line_edit_g1.text()
        # Get the selected color from the ComboBox
        selected_color = self.color_g1_combo_btn.currentText()
        self.signals_data_1[selected_item_index][2] = selected_color
        self.signals_data_1[selected_item_index][3] = label_text
        self.g_1_signals_combo_box.setItemText(selected_item_index, label_text)
        

    # A function that updates the data of the signal whenever the user change the data and press on save button in graph 2
    def save_changes_g2(self):
        if not self.signals_data_2:
            return
        selected_item_index = self.g_2_signals_combo_box.currentIndex()
        label_text = self.line_edit_g2.text()
        # Get the selected color from the ComboBox
        selected_color = self.color_g2_combo_btn.currentText()
        self.signals_data_2[selected_item_index][2] = selected_color
        self.signals_data_2[selected_item_index][3] = label_text
        self.g_2_signals_combo_box.setItemText(selected_item_index, label_text)
        

    # A function to re-index the left signals after deleting anyone
    def reindex_dict_keys(self, dictionary):
        return {i: value for i, (key, value) in enumerate(dictionary.items(), start=1)}

    # A function to refill the comboBox 
    def refill_combo_from_dict(self, combo_box, dictionary):
        combo_box.clear()  # Clear the combo box
        combo_box.addItem("Select a Signal")
        # Add items from the dictionary to the combo box
        for key in dictionary:
            combo_box.addItem(f"{'Signal'} - {key}")

    # A Function used to delete the signals from graph 1 after choosing them
    def delete_signal_g_1(self):
        if not self.signals_data_1:
            return  # No items in the dictionary to delete
        selected_item_index = self.g_1_signals_combo_box.currentIndex()
        del self.signals_data_1[selected_item_index]
        self.count_signals_1 -= 1
        self.timer_1.stop()
        self.graphicsView_1.clear()
        self.end_indx_1 = 50
        self.start_1 = 0
        self.end_1 = 616 * self.first_element_of_time
        # Reindex the dictionary keys
        self.signals_data_1 = self.reindex_dict_keys(self.signals_data_1)
        self.refill_combo_from_dict(self.g_1_signals_combo_box, self.signals_data_1)
        self.handle_graph_1(self.signals_data_1)
        self.load_data()

    # A Function used to delete the signals from graph 2 after choosing them
    def delete_signal_g_2(self):
        if not self.signals_data_2:
            return  # No items in the dictionary to delete
        selected_item_index = self.g_2_signals_combo_box.currentIndex()
        del self.signals_data_2[selected_item_index]
        self.count_signals_2 -= 1
        self.timer_2.stop()
        self.graphicsView_2.clear()
        self.end_indx_2 = 50
        self.start_2 = 0
        self.end_2 = 0.154
        # Reindex the dictionary keys
        self.signals_data_2 = self.reindex_dict_keys(self.signals_data_2)
        self.refill_combo_from_dict(self.g_2_signals_combo_box, self.signals_data_2)
        self.handle_graph_2(self.signals_data_2)
        self.load_data()

    # A Function used to move the signals from graph 1 to graph 2 after choosing them
    def move_signal_g_1(self):
        if not self.signals_data_1:
            return
        selected_item_index = self.g_1_signals_combo_box.currentIndex()
        self.count_signals_2 += 1
        self.signals_data_2[self.count_signals_2] = [self.signals_data_1[selected_item_index][0], self.signals_data_1[selected_item_index][1], 'Red',
                                                     f"{'Signal'} - {self.count_signals_2}",
                                                     True, self.signals_data_1[selected_item_index][5]]
        self.g_2_signals_combo_box.addItem(f"{'Signal'} - {self.count_signals_2}")
        self.number_of_points_2 = len(self.signals_data_1[selected_item_index][0])
        self.delete_signal_g_1()
        self.graph_1_active = True
        self.graph_2_active = True
        self.rewind_graph()
        self.graph_1_active = self.graph1_radio_btn.isChecked()
        self.graph_2_active = self.graph2_radio_btn.isChecked()
        self.load_data()

    # A Function used to move the signals from graph 1 to graph 2 after choosing them
    def move_signal_g_2(self):
        if not self.signals_data_2:
            return
        selected_item_index = self.g_2_signals_combo_box.currentIndex()
        self.count_signals_1 += 1
        self.signals_data_1[self.count_signals_1] = [self.signals_data_2[selected_item_index][0],
                                                     self.signals_data_2[selected_item_index][1], 'Red',
                                                     f"{'Signal'} - {self.count_signals_1}",
                                                     True, self.signals_data_2[selected_item_index][5]]
        self.g_1_signals_combo_box.addItem(f"{'Signal'} - {self.count_signals_1}")
        self.number_of_points_1 = len(self.signals_data_2[selected_item_index][0])
        self.delete_signal_g_2()
        self.graph_1_active = True
        self.graph_2_active = True
        self.rewind_graph()
        self.graph_1_active = self.graph1_radio_btn.isChecked()
        self.graph_2_active = self.graph2_radio_btn.isChecked()
        self.load_data()

    # A Function used to capture snapshots for the garphs and create a pdf report
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

                # Title for the PDF
                self.title_pdf()

                # Check which graph is active and create tables accordingly
                if self.graph_1_active and self.signals_data_1:
                    self.add_statistics_tables(self.signals_data_1, "Graph 1")

                    # Add statistics tables for Graph 2
                if self.graph_2_active and self.signals_data_2:
                    self.add_statistics_tables(self.signals_data_2, "Graph 2")

                # Build and save the PDF document
                doc.build(self.pdf_content)

                # Delete the temporary snapshot image
                for i in range(self.snapshot_counter):
                    self.snapshot_path = f"temp_snapshot_{i}.png"
                    os.remove(self.snapshot_path)
                self.snapshot_counter = 0

                # Clear PDF content
                self.pdf_content = []

    # Add this function to generate tables for a specific graph
    def add_table_to_pdf(self, graph_data):
        # Add a title for the table
        self.pdf_content.append(Table([[graph_data['graph_name']]], style=[
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))

        # Loop through the signal data and add tables for statistics

    def add_statistics_tables(self, graph_data, graph_name):
        for signal_index, signal_info in graph_data.items():
            time_values, signal_values, signal_color, signal_name, is_hidden, _ = signal_info

            # Check if the signal is not hidden
            if  is_hidden:
                # Proceed to add the statistics table
                mean_value = np.mean(signal_values)
                std_deviation = np.std(signal_values)
                duration = time_values[-1] - time_values[0]
                min_value = np.min(signal_values)
                max_value = np.max(signal_values)

                # Add a title for the signal
                signal_title = f"{graph_name} {signal_name}."
                self.pdf_content.append(Table([[signal_title]], style=[
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

    # A function to save the snapshot used to make the report
    def save_snap_shot(self):
        if not self.signals_data_1 and not self.signals_data_2:
            self.show_message("Graphs are empty")
            return
        if self.graph_1_active and self.graph_2_active:
            self.show_message("SnapShot taken for both Graphs")
            self.save_graph_snapshot(self.graphicsView_1, "Graph 1 & Graph 2")
            self.save_graph_snapshot(self.graphicsView_2, "Graph 1 & Graph 2")
            return
        if self.graph_1_active:
            self.show_message("SnapShot taken for Graph 1")
            self.save_graph_snapshot(self.graphicsView_1, "Graph 1")
        if self.graph_2_active:
            self.show_message("SnapShot taken for Graph 2")
            self.save_graph_snapshot(self.graphicsView_2, "Graph 2")

    # A function to determines how the snapshot of the graph is displayed
    def save_graph_snapshot(self, graphics_view, title):
        self.pdf_content.append(Table([[title]], style=[
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        # Calculate the size of the snapshot image
        plot_widget_image = QImage(graphics_view.size(), QImage.Format_ARGB32)
        plot_widget_image.fill(Qt.transparent)
        painter = QPainter(plot_widget_image)
        # Ensure that the y-axis is visible
        graphics_view.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        graphics_view.render(painter)
        painter.end()
        # Save the snapshot as a temporary image
        # Create the snapshot path with an incrementing number
        self.snapshot_path = f"temp_snapshot_{self.snapshot_counter}.png"
        plot_widget_image.save(self.snapshot_path)
        # Add the snapshot image to the PDF
        im = Image(self.snapshot_path, width=6 * inch, height=4 * inch)
        self.pdf_content.append(im)
        self.pdf_content.append(Spacer(1, 0.2 * inch))
        # Increment the counter for the next snapshot
        self.snapshot_counter += 1

    # A function that adds a title to the pdf
    def title_pdf(self):
        # Add a title for the PDF
        title = "Signal PDF Report"
        self.pdf_content.append(Table([[title]], style=[
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))

    # A function that makes graph 1 selected 
    def graph1_selected(self):
        self.graph_1_active = True
        self.graph_2_active = False

    # A function that makes graph 2 selected 
    def graph2_selected(self):
        self.graph_1_active = False
        self.graph_2_active = True

    # A function that makes both graph 1 and graph 2 selected 
    def link_selected(self):
        self.graph_1_active = True
        self.graph_2_active = True
        self.rewind_graph()

    # A function to select the speed of the graph
    def on_combobox_speed_selection(self):
        if not self.signals_data_1 and not self.signals_data_2:
            return
        speed_list = [50, 44, 38, 31, 25]
        speed_index = self.speed_selection.currentIndex() - 1
        if self.graph_1_active:
            self.timer_1.setInterval(speed_list[speed_index])
        if self.graph_2_active:
            self.timer_2.setInterval(speed_list[speed_index])

 # A function that triggers between play and pause to control the flow of signals on graph
    def play_pause(self):
        if not self.signals_data_1 and not self.signals_data_2:
            return
        if self.graph_1_active:
            self.is_playing_g_1 = not self.is_playing_g_1
            if self.is_playing_g_1:
                self.timer_1.start()
            else:
                self.timer_1.stop()
        if self.graph_2_active:
            self.is_playing_g_2 = not self.is_playing_g_2
            if self.is_playing_g_2:
                self.timer_2.start()
            else:
                self.timer_2.stop()
        # Check if both graphs are active and in sync
        if self.graph_1_active and self.graph_2_active:
            if self.is_playing_g_1:
                self.is_playing_g_2 = True
                self.timer_2.start()
            else:
                self.is_playing_g_2 = False
                self.timer_2.stop()

    # A function used to clear the graph from the signals plotted on it
    def clear_graph(self):
        if not self.signals_data_1 and not self.signals_data_2:
            return
        if self.graph_1_active:
            if not self.signals_data_1:
                self.timer_1.stop()
            self.graphicsView_1.clear()
            self.end_indx_1 = 50
            self.start_1 = 0
            self.end_1 = 0.154
        if self.graph_2_active:
            if not self.signals_data_2:
                 self.timer_2.stop()
            self.graphicsView_2.clear()
            self.end_indx_2 = 50
            self.start_2 = 0
            self.end_2 = 0.154

    # A function used to determine the ranges of the graph
    def zoom(self, graphicsView, zoom_factor):
        # Get the current visible x and y ranges
        x_min, x_max = graphicsView.getViewBox().viewRange()[0]
        y_min, y_max = graphicsView.getViewBox().viewRange()[1]
        # Calculate the new visible x and y ranges (zoom)
        new_x_min = x_min * zoom_factor
        new_x_max = x_max * zoom_factor
        new_y_min = y_min * zoom_factor
        new_y_max = y_max * zoom_factor
        # Set the new visible x and y ranges
        graphicsView.getViewBox().setRange(xRange=[new_x_min, new_x_max], yRange=[new_y_min, new_y_max])

    # A function used to zoom out from the graph
    def zoom_out(self):
        if not self.signals_data_1 and not self.signals_data_2:
            return
        if self.graph_1_active:
            if self.zoom_count_graph1 > -3:
                self.zoom(self.graphicsView_1, 0.5)
                self.zoom_count_graph1 -= 1
        if self.graph_2_active:
            if self.zoom_count_graph2 > -3:
                self.zoom(self.graphicsView_2, 0.5)
                self.zoom_count_graph2 -= 1

    # A function used to zoom in the graph
    def zoom_in(self):
        if not self.signals_data_1 and not self.signals_data_2:
            return
        if self.graph_1_active:
            if self.zoom_count_graph1 < 5:  # Set your desired limit
                self.zoom(self.graphicsView_1, 1.3)
                self.zoom_count_graph1 += 1
        if self.graph_2_active:
            if self.zoom_count_graph2 < 5:  # Set your desired limit
                self.zoom(self.graphicsView_2, 1.3)
                self.zoom_count_graph2 += 1
    
    # A function that rewinds the selected graph, making the signals plotted again
    def rewind_graph(self):
        if not self.signals_data_1 and not self.signals_data_2:
            return
        if self.graph_1_active:
            # Clear Graph for graph 1
            self.clear_graph()
            # Replot signals for graph 1
            self.handle_graph_1(self.signals_data_1)
        if self.graph_2_active:
            # Clear Graph for graph 2
            self.clear_graph()
            # Replot signals for graph 2
            self.handle_graph_2(self.signals_data_2)
        if self.graph_1_active and self.graph_2_active:
            # Both graphs are active, so rewind both
            self.clear_graph()
            self.handle_graph_1(self.signals_data_1)
            self.handle_graph_2(self.signals_data_2)

    # A function to change the value of the y-axis slider
    def onSliderValueChanged_y(self, value):
        if not self.signals_data_1 and not self.signals_data_2:
            return
        y_range_offset = 0.02 * value
        if self.graph_1_active:
            self.graphicsView_1.setYRange(-self.max_y_1 + y_range_offset, self.max_y_1 + y_range_offset)
        if self.graph_2_active:
            self.graphicsView_2.setYRange(-self.max_y_2 + y_range_offset, self.max_y_2 + y_range_offset)

    # A function to change the value of the x-axis slider
    def onSliderValueChanged_x(self, value):
        if not self.signals_data_1 and not self.signals_data_2:
            return
        x_range_offset = 0.0098 * value
        if self.graph_1_active:
            if self.end_indx_1 <= 500:
                self.graphicsView_1.setXRange(0 + x_range_offset, 0.154 + x_range_offset)
            else:
                self.graphicsView_1.setXRange(self.start_1 + x_range_offset, self.end_1 + x_range_offset)
        if self.graph_2_active:
            if self.end_indx_2 <= 500:
                self.graphicsView_2.setXRange(0 + x_range_offset, 0.154 + x_range_offset)
            else:
                self.graphicsView_2.setXRange(self.start_2 + x_range_offset, self.end_2 + x_range_offset)

    # A function to load the data of the signals in the table
    def load_data(self):
        # Clear the table
        self.tableWidget.clear()
        if not self.signals_data_1 and not self.signals_data_2:
            return

        # Define a list of statistic names
        statistic_names = ["Statistic", "Mean", "Std", "Duration", "Min", "Max"]

        # Create a dictionary to map signal indices to signal information
        signal_index_info_map = {}

        # Loop through each signal in graph 1 and populate the signal_index_info_map
        for signal_index, signal_info in self.signals_data_1.items():
            signal_index_info_map[signal_index] = ("Graph 1 " + signal_info[3], signal_info)

        # Loop through each signal in graph 2 and populate the signal_index_info_map
        for signal_index, signal_info in self.signals_data_2.items():
            signal_index_info_map[signal_index + len(self.signals_data_1)] = ("Graph 2 " + signal_info[3], signal_info)

        num_signals = len(signal_index_info_map)
        num_stats = 5  # There are 5 statistics for each signal

        self.tableWidget.setRowCount(num_signals + 1)  # Signals rows (+1 for the statistic names)
        self.tableWidget.setColumnCount(num_stats + 1)  # Statistics columns (+1 for signal labels)

        # Set the table headers for statistics and signal labels
        for col, header in enumerate(statistic_names):
            self.tableWidget.setItem(0, col, QTableWidgetItem(header))

        # Loop through each signal in the signal_index_info_map and populate the table with statistics
        for signal_index, (signal_name, signal_info) in signal_index_info_map.items():
            time_values, signal_values, signal_color, __, _, _ = signal_info
            # Calculate statistics for the current signal
            mean_value = np.mean(signal_values)
            std_deviation = np.std(signal_values)
            duration = time_values[-1] - time_values[0]
            min_value = np.min(signal_values)
            max_value = np.max(signal_values)
            # Set the signal label in the row header
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

        # Set resizing mode to make the cells occupy the full width of the table
        for col in range(self.tableWidget.columnCount()):
            self.tableWidget.horizontalHeader().setSectionResizeMode(col, QHeaderView.Stretch)

    # A function to set the window title
    def show_message(self, text, timeout=1000):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(text)
        msgBox.setWindowTitle("Signal Viewer")

        # Set up a timer to close the message box after the specified timeout (in milliseconds)
        timer = QtCore.QTimer()
        timer.setSingleShot(True)
        timer.timeout.connect(msgBox.accept)
        timer.start(timeout)

        # Show the message box
        msgBox.exec()

def main():  # method to start app
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()  # infinte Loop


if __name__ == '__main__':
    main()

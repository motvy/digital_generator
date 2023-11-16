import config
import utils

from PyQt5.QtWidgets import QLabel, QFrame, QGridLayout, QCheckBox, QHBoxLayout, QVBoxLayout, QPushButton

import pyqtgraph as pg


class ChannelsPlot():
    def __init__(self, main_window):
        self.main_window = main_window
        self.db = main_window.db

        self.live_plot = {}
        self.static_plot = {}

        self.colors = config.PLOT_COLORS
        self.plots = {}
    
    def create(self):
        self.plot_layout = QGridLayout()

        for i in range(8):
            plot_graph = utils.MyPlotWidget()
            plot_graph.clicked.connect(lambda: self.update(i))
            plot_graph.setBackground('white')

            plot_cb = QCheckBox()
            plot_cb.clicked.connect(lambda: self.set_channel_enabled())
            plot_cb.setChecked(True)

            plot_label = QLabel(str(i))
            plot_label.setStyleSheet('font-size: 10pt;')
            plot_label.setDisabled(True)

            self.plot_layout.addWidget(plot_cb, i, 0)
            self.plot_layout.addWidget(plot_label, i, 1)
            self.plot_layout.addWidget(plot_graph, i, 2)
        
        plot_frame = QFrame(self.main_window)
        plot_frame.setLayout(self.plot_layout)
        plot_frame.setFrameShape(QFrame.Panel)

        return plot_frame

    def update(self, i):
        for indx in range(self.plot_layout.count()):
            plot = self.plot_layout.itemAtPosition(indx, 2)
            item = self.plot_layout.itemAtPosition(indx, 0)

            if not item or not plot:
                break

            if plot.widget() == self.main_window.sender():
                cb = item.widget()
                cb.setChecked(not cb.isChecked())
                self.set_channel_enabled()
                break

    def set_channel_enabled(self):
        not_any_checked = True
        for indx in range(self.plot_layout.count()):
            item = self.plot_layout.itemAtPosition(indx, 0)
            label = self.plot_layout.itemAtPosition(indx, 1)
            plot = self.plot_layout.itemAtPosition(indx, 2)
            if not item or not label or not plot:
                break


            plot_graph = plot.widget()
            length = self.db.get_global_settings().length
            if indx in self.plots:
                plot_graph.removeItem(self.plots[indx])
            plot_graph.setLimits(xMin = 0.01, yMin = -0.01, xMax=length - 0.01, yMax=1.01)
            plot_graph.setMouseEnabled(x=False, y=False)
            plot_graph.getPlotItem().hideAxis('bottom')
            plot_graph.getPlotItem().hideAxis('left')

            temperature = self.static_plot[indx]['temperature']
            time = self.static_plot[indx]['time']
            if len(temperature) < len(time):
                temperature = temperature + [temperature[-1]]*2
            if item.widget().isChecked():
                not_any_checked = False
                plot_graph.setBackground('white')
                self.plots[indx] = plot_graph.plot(time, temperature, pen={'color':self.colors[indx]})
                label.widget().setDisabled(False)
            else:
                plot_graph.setBackground('#f0f0f0')
                self.plots[indx] = plot_graph.plot(time, temperature, pen={'color':'#cccccc'})
                label.widget().setDisabled(True)
        
        if not_any_checked:
            self.main_window.buttons_frame.setDisabled(True)
        else:
            self.main_window.buttons_frame.setDisabled(False)
    
    def go_plot(self, is_live=False):
        selected_channels = self.get_selected_channels()
        length = self.db.get_global_settings().length
        for i in range(8):
            plot_graph = self.plot_layout.itemAtPosition(i, 2).widget()
            if i in self.plots:
                plot_graph.removeItem(self.plots[i])

            plot_graph.setLimits(xMin = 0.01, yMin = -0.01, xMax=length - 0.01, yMax=1.01)
            plot_graph.setMouseEnabled(x=False, y=False)
            plot_graph.getPlotItem().hideAxis('bottom')
            plot_graph.getPlotItem().hideAxis('left')

            specific_settings = self.db.get_specific_pattern_settings(i)
            if is_live:
                if i not in selected_channels:
                    continue
                
                # self.live_plot[i]['temperature'] = self.live_plot[i]['temperature'][-2:] + self.live_plot[i]['temperature'][:-2]
                temperature = self.live_plot[i]['temperature']
                time = self.live_plot[i]['time']
                if len(temperature) < len(time):
                    temperature = temperature + [temperature[-1]]*2
                
                self.plots[i] = plot_graph.plot(time, temperature, pen={'color':self.colors[i]})
            else:
                time, temperature = self.generate_plot_data(length, specific_settings.period, specific_settings.k, specific_settings.delay)
                self.static_plot[i] = {'time': time, 'temperature': temperature}
            
                color = self.colors[i] if i in selected_channels else '#d6d6d6'
                self.plots[i] = plot_graph.plot(time, temperature, pen={'color':color})
                if temperature[:2] == [0, 0]:
                    if temperature[-2:] ==  [1, 0]:
                        self.live_plot[i] = {'time': time, 'temperature': temperature[2:]}
                    elif temperature[-2:] == [1, 1]:
                        temperature[-1] = 0
                        self.live_plot[i] = {'time': time, 'temperature': temperature[2:]}
                    else:
                        self.live_plot[i] = {'time': time, 'temperature': temperature[:-2]}
                else:
                    if temperature[-2:] == [0, 0]:
                        self.live_plot[i] = {'time': time, 'temperature': temperature[2:]}
                    elif temperature[-2:] == [0, 1]:
                        temperature[0] = 0
                        self.live_plot[i] = {'time': time, 'temperature': temperature[:-2]}
                    else:
                        self.live_plot[i] = {'time': time, 'temperature': temperature[:-2]}


    def generate_plot_data(self, length, period, k, delay):
        temperature = [0] * (delay * 2)
        if k == 100:
            up = [1] * (length - delay + 1)
            low = []
            if temperature:
                temperature.append(0)
        elif k == 0:
            up = []
            low = [0] * (length - delay + 1)
        else:
            count = period*2 - 2

            k_up = (2 + count) * k // 100 - 1
            k_low = count - k_up
            up = [0, 1] + [1, 1] * (k_up)
            low = [1, 0] + [0, 0] * (k_low)
     

        time = [i // 2 for i in range(0, (length+1)*2)]
        while len(temperature) < len(time):
            temperature.extend(low)
            temperature.extend(up)

        if delay and length > delay:
            temperature[delay * 2] = 0
        temperature = temperature[:len(time)]

        return time, temperature

    def get_selected_channels(self):
        channels = []
        for indx in range(self.plot_layout.count()):
            item = self.plot_layout.itemAtPosition(indx, 0)
            if not item:
                break

            if item.widget().isChecked():
                channels.append(indx)
        
        return channels
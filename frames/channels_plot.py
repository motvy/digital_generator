import config

from PyQt5.QtWidgets import QLabel, QFrame, QGridLayout, QCheckBox, QVBoxLayout

import pyqtgraph as pg


class ChannelsPlot():
    def __init__(self, main_window):
        self.main_window = main_window
        self.db = main_window.db

        self.colors = config.PLOT_COLORS
        self.plots = {}
    
    def create(self):
        self.plot_layout = QGridLayout()

        for i in range(8):
            plot_graph = pg.PlotWidget()
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

    def set_channel_enabled(self):
        not_any_checked = True
        for indx in range(self.plot_layout.count()):
            item = self.plot_layout.itemAtPosition(indx, 0)
            label = self.plot_layout.itemAtPosition(indx, 1)
            plot = self.plot_layout.itemAtPosition(indx, 2)
            if not item or not label or not plot:
                break

            if item.widget().isChecked():
                not_any_checked = False
                plot.widget().setBackground('white')
                label.widget().setDisabled(False)
            else:
                plot.widget().setBackground('#e0e0e0')
                label.widget().setDisabled(True)
        
        if not_any_checked:
            self.main_window.buttons_frame.setDisabled(True)
        else:
            self.main_window.buttons_frame.setDisabled(False)
    
    def go_plot(self):
        length = self.db.get_global_settings().length
        for i in range(8):
            plot_graph = self.plot_layout.itemAtPosition(i, 2).widget()
            if i in self.plots:
                plot_graph.removeItem(self.plots[i])

            plot_graph.setLimits(xMin = -0.01, yMin = -0.01, xMax=length + 0.01, yMax=1.01)
            plot_graph.setMouseEnabled(x=False, y=False)
            plot_graph.getPlotItem().hideAxis('bottom')
            plot_graph.getPlotItem().hideAxis('left')

            specific_settings = self.db.get_specific_pattern_settings(i)
            time, temperature = self.generate_plot_data(length, specific_settings.period, specific_settings.k, specific_settings.delay)
            self.plots[i] = plot_graph.plot(time, temperature, pen={'color':self.colors[i]})


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
            count = 0 if period == 1 else 2**(period-1)

            k_up = (2 + count) * k // 100 - 1
            k_low = count - k_up
            up = [0, 1] + [1, 1] * (k_up)
            low = [1, 0] + [0, 0] * (k_low)
     

        time = [i // 2 for i in range(0, (length+1)*2)]
        while len(temperature) < len(time):
            temperature.extend(up)
            temperature.extend(low)

        temperature = temperature[:len(time)]

        if temperature[-2:] == [0, 1]:
            temperature[-1] = 0

        return time, temperature
import config

from PyQt5.QtWidgets import QLabel, QFrame, QGridLayout, QCheckBox, QVBoxLayout

import pyqtgraph as pg


class ChannelsPlot():
    def __init__(self, main_window):
        self.main_window = main_window

        self.colors = config.PLOT_COLORS
    
    def create(self):
        self.plot_layout = QGridLayout()

        for i in range(8):
            plot_graph = pg.PlotWidget()
            plot_graph.setLimits(xMin = -0.01, yMin = -1, xMax=6.01, yMax=2)
            plot_graph.setMouseEnabled(x=False, y=False)
            
            plot_graph.getPlotItem().hideAxis('bottom')
            plot_graph.getPlotItem().hideAxis('left')
            time = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6]
            temperature = [0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1]
            plot_graph.plot(time, temperature, pen={'color':self.colors[i]})
            plot_graph.setBackground('#e0e0e0')

            plot_cb = QCheckBox()
            plot_cb.clicked.connect(self.set_channel_enabled)

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
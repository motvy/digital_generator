"""
Зависимости:
Задержка < Длина
Полупериод < Длина
Период < длины

"""

from customs import NewQAbstractSpinBox, stylesheet
from global_settings import GlobalSettings
from specific_settings import SpecificSettings
from channels_plot import ChannelsPlot

import sys
import datetime

from PyQt5 import QtCore
from PyQt5.QtCore import QSize, Qt, QTimer
from PyQt5.QtGui import QFont, QIntValidator
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QDoubleSpinBox, QSpinBox,\
      QLineEdit, QPushButton, QFrame, QTabWidget, QTableWidget, QTableWidget, QTableWidgetItem, QAbstractItemView, QCheckBox, QWidget, QGridLayout, \
      QAbstractSpinBox


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet(stylesheet)

        self.setWindowTitle("Digital generator")
        self.setFixedSize(QSize(1440, 810))

        self.initUI()
        self.initData()

    def initUI(self):
        self.global_settings = GlobalSettings(self)
        self.specific_settings = SpecificSettings(self)
        self.chanels_plot = ChannelsPlot(self)

        settings_layout = QVBoxLayout()
        settings_layout.addWidget(self.global_settings.create())
        settings_layout.addWidget(self.specific_settings.create())

        parameters_layout = QHBoxLayout()
        parameters_layout.addWidget(self.chanels_plot.create())
        parameters_layout.addLayout(settings_layout)

        self.parameters_frame = QFrame(self)
        self.parameters_frame.setLayout(parameters_layout)
        self.parameters_frame.setFrameShape(QFrame.Panel)

        self.buttons_frame = self.main_buttons()
        self.buttons_frame.setDisabled(True)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.parameters_frame)
        main_layout.addWidget(self.buttons_frame)
        self.setLayout(main_layout)

    def start_generate(self):
        self.start_timer()
        self.start_button.setText('Стоп')
        self.start_button.clicked.connect(self.stop_generate)
        self.parameters_frame.setEnabled(False)

    def stop_generate(self):
        self.stop_timer()
        self.start_button.setText('Старт')
        self.start_button.clicked.connect(self.start_generate)
        self.parameters_frame.setEnabled(True)

    def main_buttons(self):
        self.timer_count = 0
        self.timer_flag = False
        timer = QTimer(self)
        timer.timeout.connect(self.show_time)
        timer.start(1000)

        self.timer_label = QLabel()
        self.timer_label.setText(str(datetime.timedelta(seconds=0)))
        self.timer_label.setStyleSheet('font-size: 10pt;')

        self.start_button = QPushButton('Старт')
        self.start_button.setMinimumWidth(270)
        self.start_button.clicked.connect(self.start_generate)

        current_layout = QHBoxLayout()
        current_layout.addWidget(self.timer_label)
        current_layout.addStretch(1)
        current_layout.addWidget(self.start_button)
        buttons_frame = QFrame(self)
        buttons_frame.setLayout(current_layout)

        return buttons_frame

    def show_time(self):
        if self.timer_flag:
            self.timer_count+= 1
 
        self.timer_label.setText(str(datetime.timedelta(seconds=self.timer_count)))
 
    def start_timer(self):
        self.timer_flag = True
 
    def stop_timer(self):
        self.timer_flag = False
        self.timer_count = 0
        self.timer_label.setText(str(datetime.timedelta(seconds=self.timer_count)))

    def initData(self):
        pass


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
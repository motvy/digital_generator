"""
Зависимости:
Задержка < Длина
Полупериод < Длина
Период < длины

"""

from utils import stylesheet
import config
from frames.global_settings import GlobalSettings
from frames.specific_settings import SpecificSettings
from frames.channels_plot import ChannelsPlot
from settingsdb import SettingsDb

import datetime
import time
import serial

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, QTimer
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QWidget, QMessageBox


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.db = SettingsDb()

        self.setStyleSheet(stylesheet)

        self.setWindowTitle("Генератор цифровых последовательностей")
        # self.setFixedSize(QSize(1440, 810))
        self.setFixedSize(QSize(1200, 700))

        self.setWindowIcon(QIcon(config.app_icon_path))

        self.ser = serial.Serial('COM1', 9600, timeout=1)

        self.initUI()
        self.initData()
        self.parameters_frame.setEnabled(False)
        self.start_button.setEnabled(False)
        self.start_timer("Ожидается команда от МК...")

    def initUI(self):
        self.chanels_plot = ChannelsPlot(self)
        self.global_settings = GlobalSettings(self)
        self.specific_settings = SpecificSettings(self)

        parameters_layout = QHBoxLayout()
        parameters_layout.addWidget(self.chanels_plot.create())

        settings_layout = QVBoxLayout()
        settings_layout.addWidget(self.global_settings.create())
        settings_layout.addWidget(self.specific_settings.create())

        parameters_layout.addLayout(settings_layout)

        self.parameters_frame = QFrame(self)
        self.parameters_frame.setLayout(parameters_layout)
        self.parameters_frame.setFrameShape(QFrame.Panel)

        self.buttons_frame = self.main_buttons()
        self.buttons_frame.setDisabled(False)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.parameters_frame)
        main_layout.addWidget(self.buttons_frame)
        self.setLayout(main_layout)

    def regenerate_plot(self, is_live=False):
        self.chanels_plot.go_plot(self.specific_settings.current_mode, is_live)

    def get_settings_list(self):
        settings = self.db.get_global_settings()
        length_h = settings.length // 256
        length_l = settings.length % 256

        amplitude = int(settings.amplitude * 255 / 49.5)

        return [length_h, length_l, amplitude, config.FREQUENCY_LIST.index(settings.frequency), settings.frequency_source]

    def start_generate(self):
        self.start_button.clicked.disconnect()
        self.start_button.setEnabled(False)
        if self.global_settings.hasUnsaved() or self.specific_settings.hasUnsaved():
            QMessageBox.critical(self, 'Генератор цифровых последовательностей', 'Генерация невозможна. Не все параметры применены.')
            self.start_button.setEnabled(True)
            self.start_button.clicked.connect(self.start_generate)
        else:
            self.parameters_frame.setEnabled(False)
            # self.regenerate_plot(True)

            settings = self.get_settings_list()
            settings_arr = bytearray(settings)
            self.ser.write(settings_arr)

            print(settings)


            data = self.chanels_plot.get_plots_data()[1]

            print(data)

            for i in range(0, len(data), 512):
                data_arr = bytearray(data[i:i+512])
                self.ser.write(data_arr)
                time.sleep(0.7)


            # data_arr1 = bytearray(data[:255])
            # data_arr2 = bytearray(data[255:])
            # self.ser.write(bytearray(data))
            # self.ser.write(data_arr1)
            # self.ser.write(data_arr2)
            # import time
            # time.sleep(5)
            line = self.ser.readline()
            if line:
                self.start_timer("Генерация в процессе. Для изменения параметров воспользуйтесь кнопкой на МК.")
                self.start_button.clicked.connect(self.start_generate)
            else:
                self.timer_label.setText("")
                QMessageBox.critical(self, 'Генератор цифровых последовательностей', 'МК не отвечает. Попробуйте снова.')
                self.parameters_frame.setEnabled(True)
                self.start_button.setEnabled(True)
                self.start_button.clicked.connect(self.start_generate)

            # self.start_button.setText('Стоп')
            # self.start_button.clicked.disconnect()
            # self.start_button.clicked.connect(self.stop_generate)
            # self.parameters_frame.setEnabled(False)
            # self.start_button.setEnabled(False)

    # def stop_generate(self):
    #     self.stop_timer()
    #     self.start_button.setText('Старт')
    #     self.start_button.clicked.disconnect()
    #     self.start_button.clicked.connect(self.start_generate)
    #     self.regenerate_plot()
    #     self.parameters_frame.setEnabled(True)

    def main_buttons(self):
        # self.timer_count = 0
        self.timer_flag = False
        timer = QTimer(self)
        timer.timeout.connect(self.show_time)
        timer.start(1000)

        self.timer_label = QLabel()
        # self.timer_label.setText(str(datetime.timedelta(seconds=0)))
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
            line = self.ser.readline()
            # print(line)
            if line:
                self.stop_timer()
            # self.timer_count+= 1
 
        # self.timer_label.setText(str(datetime.timedelta(seconds=self.timer_count)))
 
    # def show_plot(self):
    #     if self.timer_flag:
    #         self.regenerate_plot(True)

    def start_timer(self, label):
        self.timer_label.setText(label)
        self.timer_flag = True
 
    def stop_timer(self):
        self.timer_label.setText("")
        self.timer_flag = False
        self.parameters_frame.setEnabled(True)
        self.start_button.setEnabled(True)
        # self.timer_count = 0
        # self.timer_label.setText(str(datetime.timedelta(seconds=self.timer_count)))

    def initData(self):
        self.global_settings.initData()
        self.specific_settings.initData()
        self.regenerate_plot()

        # plot_timer = QTimer(self)
        # plot_timer.timeout.connect(self.show_plot)
        # plot_timer.start(10)

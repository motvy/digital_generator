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

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, QTimer
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QWidget, QMessageBox


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.db = SettingsDb()

        self.setStyleSheet(stylesheet)

        self.setWindowTitle("Digital generator")
        self.setFixedSize(QSize(1440, 810))

        self.setWindowIcon(QIcon(config.app_icon_path))

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
        self.buttons_frame.setDisabled(False)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.parameters_frame)
        main_layout.addWidget(self.buttons_frame)
        self.setLayout(main_layout)

    def regenerate_plot(self, is_live=False):
        self.chanels_plot.go_plot(is_live)

    def start_generate(self):
        if self.global_settings.hasUnsaved() or self.specific_settings.hasUnsaved():
            QMessageBox.critical(self, 'Digital generator', 'Генерация невозможна. Не все параметры применены.')
            pass
        else:
            self.start_timer()
            self.start_button.setText('Стоп')
            self.start_button.clicked.disconnect()
            self.start_button.clicked.connect(self.stop_generate)
            self.parameters_frame.setEnabled(False)

    def stop_generate(self):
        self.stop_timer()
        self.start_button.setText('Старт')
        self.start_button.clicked.disconnect()
        self.start_button.clicked.connect(self.start_generate)
        self.regenerate_plot()
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
 
    def show_plot(self):
        if self.timer_flag:
            self.regenerate_plot(True)

    def start_timer(self):
        self.timer_flag = True
 
    def stop_timer(self):
        self.timer_flag = False
        self.timer_count = 0
        self.timer_label.setText(str(datetime.timedelta(seconds=self.timer_count)))

    def initData(self):
        self.global_settings.initData()
        self.specific_settings.initData()
        self.regenerate_plot()

        plot_timer = QTimer(self)
        plot_timer.timeout.connect(self.show_plot)
        plot_timer.start(250)

# app = QApplication(sys.argv)

# window = MainWindow()
# window.show()

# app.exec()
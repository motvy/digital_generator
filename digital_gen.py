import sys
import datetime
import pyqtgraph as pg

from PyQt5 import QtCore
from PyQt5.QtCore import QSize, Qt, QTimer
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QDoubleSpinBox, QSpinBox,\
      QLineEdit, QPushButton, QFrame, QTabWidget, QTableWidget, QTableWidget, QTableWidgetItem, QAbstractItemView, QCheckBox, QWidget, QGridLayout


# Subclass QMainWindow to customize your application's main window
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        stylesheet = """

        QTabWidget::pane { /* The tab widget frame */
            border-top: 0px solid black;
            position: absolute;
            top: -0.09em;
        }
        QTabBar::tab:!selected {
            border-top: 1px solid black;
            border-left: 1px solid black;
            border-right: 1px solid black;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            min-width: 10ex;
            padding: 3px;
            margin-right: 1px;
        }

        QTabBar::tab:selected {
            border-top: 1px solid black;
            border-left: 1px solid black;
            border-right: 1px solid black;
            border-bottom: 2px solid #f0f0f0;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            min-width: 10ex;
            padding: 3px;
            margin-right: 1px;
        }
        """

        self.colors = ['black', 'red', 'orange', 'brown', 'green', 'blue', 'indigo', 'violet']
        
        self.setStyleSheet(stylesheet)

        self.setWindowTitle("Digital generator")
        self.setFixedSize(QSize(1440, 810))

        self.initUI()
        self.initData()

    def initUI(self):
        settings_layout = QVBoxLayout()
        settings_layout.addWidget(self.global_settings())
        settings_layout.addWidget(self.specific_settings())

        parameters_layout = QHBoxLayout()
        parameters_layout.addWidget(self.plot())
        # parameters_layout.addStretch(1)
        parameters_layout.addLayout(settings_layout)

        self.parameters_frame = QFrame(self)
        self.parameters_frame.setLayout(parameters_layout)
        self.parameters_frame.setFrameShape(QFrame.Panel)

        buttons_frame = self.main_buttons()

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.parameters_frame)
        main_layout.addWidget(buttons_frame)
        self.setLayout(main_layout)

        # specific_settings_layout = self.specific_settings()

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

    def global_settings(self):
        frequency_label = QLabel('Частота (Гц)')
        self.frequency_input = QLineEdit()

        amplitude_label = QLabel('Ампитуда (В)')
        self.amplitude_input = QDoubleSpinBox()
        self.amplitude_input.setValue(1.8)
        self.amplitude_input.setMinimum(1.8)
        self.amplitude_input.setMaximum(4.3)
        self.amplitude_input.setSingleStep(0.1)
        self.amplitude_input.lineEdit().setReadOnly(True)

        length_label = QLabel('Длина')
        self.length_input = QLineEdit()

        reset_button = QPushButton('Сброс')
        reset_button.clicked.connect(self.reset_global_settings)
        apply_button = QPushButton('Применить')
        apply_button.clicked.connect(self.apply_global_settings)
        button_layout = QHBoxLayout()
        button_layout.addWidget(reset_button)
        button_layout.addWidget(apply_button)

        global_settings_layout = QVBoxLayout()
        global_settings_layout.addWidget(frequency_label)
        global_settings_layout.addWidget(self.frequency_input)
        global_settings_layout.addWidget(amplitude_label)
        global_settings_layout.addWidget(self.amplitude_input)
        global_settings_layout.addWidget(length_label)
        global_settings_layout.addWidget(self.length_input)
        global_settings_layout.addStretch(1)
        global_settings_layout.addLayout(button_layout)

        global_settings_frame = QFrame(self)
        global_settings_frame.setLayout(global_settings_layout)
        global_settings_frame.setFrameShape(QFrame.Panel)
        global_settings_frame.setFixedWidth(270)
        global_settings_frame.setFixedHeight(300)

        return global_settings_frame

    def reset_global_settings(self):
        pass

    def apply_global_settings(self):
        pass

    def specific_settings(self):
        specific_settings_pattern_layout = self.specific_pattern_settings()
        specific_settings_user_layout = self.specific_user_settings()

        specific_settings_pattern_frame = QFrame(self)
        specific_settings_pattern_frame.setLayout(specific_settings_pattern_layout)
        specific_settings_pattern_frame.setFrameShape(QFrame.Panel)
        specific_settings_user_frame = QFrame(self)
        specific_settings_user_frame.setLayout(specific_settings_user_layout)
        specific_settings_user_frame.setFrameShape(QFrame.Panel)

        specific_settings_tab = QTabWidget()
        specific_settings_tab.addTab(specific_settings_pattern_frame, 'Pattern')
        specific_settings_tab.addTab(specific_settings_user_frame, 'User')
        specific_settings_tab.setMaximumWidth(270)
        specific_settings_tab.setMinimumWidth(270)

    
        return specific_settings_tab

    def specific_pattern_settings(self):
        chanel_label = QLabel('Выбранные каналы')
        self.chanel_input = QLineEdit()
        self.chanel_input.setReadOnly(True)
        period_label = QLabel('Период')
        self.period_input = QLineEdit()

        k_label = QLabel('Коэффициент заполнения (%)')
        self.k_input = QSpinBox()
        self.k_input.setValue(0)
        self.k_input.setMinimum(0)
        self.k_input.setMaximum(100)
        self.k_input.setSingleStep(10)
        self.k_input.lineEdit().setReadOnly(True)

        delay_label = QLabel('Задержка')
        self.delay_input = QLineEdit()

        reset_button = QPushButton('Сброс')
        reset_button.clicked.connect(self.reset_global_settings)
        apply_button = QPushButton('Применить')
        apply_button.clicked.connect(self.apply_global_settings)
        button_layout = QHBoxLayout()
        button_layout.addWidget(reset_button)
        button_layout.addWidget(apply_button)

        specific_settings_pattern_layout = QVBoxLayout()
        specific_settings_pattern_layout.addWidget(chanel_label)
        specific_settings_pattern_layout.addWidget(self.chanel_input)
        specific_settings_pattern_layout.addWidget(k_label)
        specific_settings_pattern_layout.addWidget(self.k_input)
        specific_settings_pattern_layout.addWidget(delay_label)
        specific_settings_pattern_layout.addWidget(self.delay_input)
        specific_settings_pattern_layout.addWidget(period_label)
        specific_settings_pattern_layout.addWidget(self.period_input)
        specific_settings_pattern_layout.addStretch(1)
        specific_settings_pattern_layout.addLayout(button_layout)

        return specific_settings_pattern_layout

    def set_chanel_input(self, i):
        print('!!!!!!!', i)

    def specific_user_settings(self):
        specific_settings_user_layout = QVBoxLayout()

        return specific_settings_user_layout

    def plot(self):
        self.plot_layout = QGridLayout()


        for i in range(8):
            plot_graph = pg.PlotWidget()
            plot_graph.setLimits(xMin = 0, yMin = -1, xMax=6, yMax=2)
            plot_graph.setMouseEnabled(x=False, y=False)
            
            plot_graph.getPlotItem().hideAxis('bottom')
            plot_graph.getPlotItem().hideAxis('left')
            time = [0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6]
            temperature = [0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0]
            plot_graph.plot(time, temperature, pen={'color':self.colors[i]})
            plot_graph.setBackground('white')

            plot_cb = QCheckBox()
            plot_cb.clicked.connect(lambda: self.set_chanel_input(i))

            plot_label = QLabel(str(i))

            self.plot_layout.addWidget(plot_cb, i, 0)
            self.plot_layout.addWidget(plot_label, i, 1)
            self.plot_layout.addWidget(plot_graph, i, 2)


        plot_frame = QFrame(self)
        plot_frame.setLayout(self.plot_layout)
        plot_frame.setFrameShape(QFrame.Panel)

        return plot_frame

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
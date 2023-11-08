from utils import NewQAbstractSpinBox
import config

from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame


class GlobalSettings():
    def __init__(self, main_window):
        self.main_window = main_window
        self.db = main_window.db
        self.db_settings_dict = {}
    
    def create(self):
        self.frequency_label = QLabel('Частота (Гц)')
        self.frequency_input = QLineEdit()
        self.frequency_input.textChanged.connect(lambda: self.change_frequency())

        self.amplitude_label = QLabel('Ампитуда (В)')
        self.amplitude_input = NewQAbstractSpinBox()
        self.amplitude_input.lineEdit().textChanged.connect(lambda: self.change_amplitude())
        self.amplitude_input.lineEdit().setReadOnly(True)

        self.length_label = QLabel('Длина')
        self.length_input = QLineEdit()
        self.length_input.textChanged.connect(lambda: self.change_length())

        reset_button = QPushButton('Сброс')
        reset_button.clicked.connect(self.reset_settings)
        apply_button = QPushButton('Применить')
        apply_button.clicked.connect(self.apply_settings)
        button_layout = QHBoxLayout()
        button_layout.addWidget(reset_button)
        button_layout.addWidget(apply_button)

        settings_layout = QVBoxLayout()
        settings_layout.addWidget(self.frequency_label)
        settings_layout.addWidget(self.frequency_input)
        settings_layout.addWidget(self.amplitude_label)
        settings_layout.addWidget(self.amplitude_input)
        settings_layout.addWidget(self.length_label)
        settings_layout.addWidget(self.length_input)
        settings_layout.addStretch(1)
        settings_layout.addLayout(button_layout)

        settings_frame = QFrame(self.main_window)
        settings_frame.setLayout(settings_layout)
        settings_frame.setFrameShape(QFrame.Panel)
        settings_frame.setFixedWidth(270)
        settings_frame.setFixedHeight(230)

        return settings_frame

    def change_frequency(self):
        if int(self.frequency_input.text()) != self.db_settings_dict['frequency']:
            self.frequency_label.setText(self.frequency_label.text().strip('*') + '*')
        else:
            self.frequency_label.setText(self.frequency_label.text().strip('*'))

    def change_length(self):
        if int(self.length_input.text()) != self.db_settings_dict['length']:
            self.length_label.setText(self.length_label.text().strip('*') + '*')
        else:
            self.length_label.setText(self.length_label.text().strip('*'))

    def change_amplitude(self):
        if self.amplitude_input.value()*10 != self.db_settings_dict['amplitude']:
            self.amplitude_label.setText(self.amplitude_label.text().strip('*') + '*')
        else:
            self.amplitude_label.setText(self.amplitude_label.text().strip('*'))  

    def reset_settings(self):
        self.frequency_input.setText(str(config.DEFAULT_GLOBAL_SETTINGS['frequency']['default']))
        self.length_input.setText(str(config.DEFAULT_GLOBAL_SETTINGS['length']['default']))
        self.amplitude_input.setValue(str(config.DEFAULT_GLOBAL_SETTINGS['amplitude']['default'] / 10.0))

        self.apply_settings()

    def apply_settings(self):
        amplitude = int(self.amplitude_input.value()*10)
        if amplitude != self.db_settings_dict['amplitude']:
            self.db_settings_dict['amplitude'] = amplitude
            self.amplitude_label.setText(self.amplitude_label.text().strip('*'))  
            self.db.set_global_amplitude(amplitude)
        
        length = int(self.length_input.text())
        if length != self.db_settings_dict['length']:
            self.db_settings_dict['length'] = length
            self.length_label.setText(self.length_label.text().strip('*'))  
            self.db.set_global_length(length)

        frequency = int(self.frequency_input.text())
        if frequency != self.db_settings_dict['frequency']:
            self.db_settings_dict['frequency'] = frequency
            self.frequency_label.setText(self.frequency_label.text().strip('*'))
            self.db.set_global_frequency(frequency)
    
    def initData(self):
        db_settings = self.db.get_global_settings()
        self.db_settings_dict = db_settings._asdict()

        self.frequency_input.setText(str(db_settings.frequency))
        self.frequency_input.setValidator(QIntValidator(config.DEFAULT_GLOBAL_SETTINGS['frequency']['min'], config.DEFAULT_GLOBAL_SETTINGS['frequency']['max'], self.main_window))
        self.length_input.setText(str(db_settings.length))
        self.length_input.setValidator(QIntValidator(config.DEFAULT_GLOBAL_SETTINGS['length']['min'], config.DEFAULT_GLOBAL_SETTINGS['length']['max'], self.main_window))
        self.amplitude_input.setRange([x / 10.0 for x in range(config.DEFAULT_GLOBAL_SETTINGS['amplitude']['min'], config.DEFAULT_GLOBAL_SETTINGS['amplitude']['max'] + 1, 1)])
        self.amplitude_input.setValue(db_settings.amplitude / 10.0)








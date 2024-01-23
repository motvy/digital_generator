from utils import NewQAbstractSpinBox
import config

from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QComboBox


class GlobalSettings():
    def __init__(self, main_window):
        self.main_window = main_window
        self.db = main_window.db
        self.db_settings_dict = {}
    
    def create(self):
        self.frequency_label = QLabel('Частота (Гц)')
        self.frequency_input = NewQAbstractSpinBox()
        self.frequency_input.lineEdit().textChanged.connect(lambda: self.change_frequency())
        self.frequency_input.lineEdit().setReadOnly(True)

        # self.frequency_source_label = QLabel('Источник')
        # self.frequency_source_input = QComboBox()
        # self.frequency_source_input.currentTextChanged.connect(lambda: self.change_frequency_source())

        self.amplitude_label = QLabel('Ампитуда (В)')
        self.amplitude_input = NewQAbstractSpinBox()
        self.amplitude_input.lineEdit().textChanged.connect(lambda: self.change_amplitude())
        self.amplitude_input.lineEdit().setReadOnly(True)

        self.length_label = QLabel('Длина')
        self.length_input = QLineEdit()
        self.length_input.textChanged.connect(lambda: self.change_length())

        reset_button = QPushButton('По умолчанию')
        reset_button.clicked.connect(self.reset_settings)
        apply_button = QPushButton('Применить')
        apply_button.clicked.connect(self.apply_settings)
        button_layout = QHBoxLayout()
        button_layout.addWidget(reset_button)
        button_layout.addWidget(apply_button)

        settings_layout = QVBoxLayout()
        settings_layout.addWidget(self.frequency_label)
        settings_layout.addWidget(self.frequency_input)
        # settings_layout.addWidget(self.frequency_source_label)
        # settings_layout.addWidget(self.frequency_source_input)
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
        settings_frame.setFixedHeight(185)

        return settings_frame

    def change_frequency(self):
        if 'frequency' not in self.db_settings_dict:
            return

        if 0 < self.frequency_input.value() < 1000:
            self.frequency_label.setText("Частота (Гц)")
        elif 1000 <= self.frequency_input.value() < 1000000:
            self.frequency_label.setText("Частота (КГц)")
            self.frequency_input.lineEdit().setText(str(int(self.frequency_input.value() // 1000)))
        elif 1000000 <= self.frequency_input.value() < 8000000:
            self.frequency_label.setText("Частота (МГц)")
            self.frequency_input.lineEdit().setText(str(int(self.frequency_input.value() // 1000000)))

        if self.frequency_input.value() != self.db_settings_dict['frequency']:
            self.frequency_label.setText(self.frequency_label.text().strip('*') + '*')
        else:
            self.frequency_label.setText(self.frequency_label.text().strip('*'))  


    def change_frequency_source(self):
        if 'frequency_source' not in self.db_settings_dict:
            return

        # if self.frequency_source_input.currentIndex() != self.db_settings_dict['frequency_source']:
        #     self.frequency_source_label.setText(self.frequency_source_label.text().strip('*') + '*')
        # else:
        #     self.frequency_source_label.setText(self.frequency_source_label.text().strip('*'))

    def change_length(self):
        if 'length' not in self.db_settings_dict:
            return

        if not self.length_input.text() or int(self.length_input.text()) != self.db_settings_dict['length']:
            self.length_label.setText(self.length_label.text().strip('*') + '*')
        else:
            self.length_label.setText(self.length_label.text().strip('*'))

    def change_amplitude(self):
        if 'amplitude' not in self.db_settings_dict:
            return 

        if self.amplitude_input.value()*10 != self.db_settings_dict['amplitude']:
            self.amplitude_label.setText(self.amplitude_label.text().strip('*') + '*')
        else:
            self.amplitude_label.setText(self.amplitude_label.text().strip('*'))  

    def reset_settings(self):
        # self.frequency_source_input.setCurrentIndex(config.DEFAULT_GLOBAL_SETTINGS['frequency_source']['default'])
        self.frequency_input.setValue(config.DEFAULT_GLOBAL_SETTINGS['frequency']['default'])
        self.length_input.setText(str(config.DEFAULT_GLOBAL_SETTINGS['length']['default']))
        self.amplitude_input.setValue(str(config.DEFAULT_GLOBAL_SETTINGS['amplitude']['default'] / 10.0))

        self.apply_settings()

    def apply_settings(self):
        try:
            # frequency_source = self.frequency_source_input.currentIndex()
            # if frequency_source != self.db_settings_dict['frequency_source']:
            #     self.db_settings_dict['frequency_source'] = frequency_source
            #     self.frequency_source_label.setText(self.frequency_source_label.text().strip('*'))
            #     self.db.set_global_frequency_source(frequency_source)

            amplitude = int(self.amplitude_input.value()*10)
            if amplitude != self.db_settings_dict['amplitude']:
                self.db_settings_dict['amplitude'] = amplitude
                self.amplitude_label.setText(self.amplitude_label.text().strip('*'))
                self.db.set_global_amplitude(amplitude)
            
            length = self.length_input.text()
            if not length or int(length) < config.DEFAULT_GLOBAL_SETTINGS['length']['min']:
                length = config.DEFAULT_GLOBAL_SETTINGS['length']['min']
            elif int(length) > config.DEFAULT_GLOBAL_SETTINGS['length']['max']:
                length = config.DEFAULT_GLOBAL_SETTINGS['length']['max']
            else:
                length = int(length)
            self.length_input.setText(str(length))
            if length != self.db_settings_dict['length']:
                self.db_settings_dict['length'] = length
                self.length_label.setText(self.length_label.text().strip('*'))  
                self.db.set_global_length(length)
                if self.main_window.specific_settings.current_mode == 0:
                    self.main_window.specific_settings.pattern_settings.change_global_length()

            frequency = self.frequency_input.value()
            if frequency != self.db_settings_dict['frequency']:
                self.db_settings_dict['frequency'] = frequency
                self.frequency_label.setText(self.frequency_label.text().strip('*'))
                self.db.set_global_frequency(frequency)

        except Exception as err:
            print(err)
        finally:
            self.main_window.regenerate_plot()
    
    def initData(self):
        db_settings = self.db.get_global_settings()
        # self.db_settings_dict = db_settings._asdict()

        # self.frequency_source_input.addItems(['Внутренний генератор', 'Внешний генератор'])
        # self.frequency_source_input.setCurrentIndex(db_settings.frequency_source)
        self.db_settings_dict['frequency_source'] = db_settings.frequency_source
        # self.frequency_input.setText(str(db_settings.frequency))
        self.db_settings_dict['frequency'] = db_settings.frequency
        # self.frequency_input.setValidator(QIntValidator(config.DEFAULT_GLOBAL_SETTINGS['frequency']['min'], config.DEFAULT_GLOBAL_SETTINGS['frequency']['max'], self.main_window))
        self.length_input.setText(str(db_settings.length))
        self.db_settings_dict['length'] = db_settings.length
        self.length_input.setValidator(QIntValidator(config.DEFAULT_GLOBAL_SETTINGS['length']['min'], config.DEFAULT_GLOBAL_SETTINGS['length']['max'], self.main_window))
        self.frequency_input.setRange(config.FREQUENCY_LIST)
        self.frequency_input.setValue(db_settings.frequency)
        self.amplitude_input.setRange([x / 10.0 for x in range(config.DEFAULT_GLOBAL_SETTINGS['amplitude']['min'], config.DEFAULT_GLOBAL_SETTINGS['amplitude']['max'] + 1, 1)])
        self.amplitude_input.setValue(db_settings.amplitude / 10.0)
        self.db_settings_dict['amplitude'] = db_settings.amplitude

    def hasUnsaved(self):
        for label in (self.frequency_label, self.length_label, self.amplitude_label):
            if '*' in label.text():
                return True
        return False

from customs import NewQAbstractSpinBox

from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QTabWidget, QSpinBox, QCheckBox, QGridLayout


class SpecificSettings():
    def __init__(self, main_window):
        self.main_window = main_window
    
    def create(self):
        pattern_settings = PatternSpecificSettings(self)
        user_settings = UserSpecificSettings(self)
        pattern_layout = pattern_settings.create()
        user_layout = user_settings.create()

        pattern_frame = QFrame(self.main_window)
        pattern_frame.setLayout(pattern_layout)
        pattern_frame.setFrameShape(QFrame.Panel)
        user_frame = QFrame(self.main_window)
        user_frame.setLayout(user_layout)
        user_frame.setFrameShape(QFrame.Panel)

        settings_tab = QTabWidget()
        settings_tab.addTab(pattern_frame, 'Pattern')
        settings_tab.addTab(user_frame, 'User')
        settings_tab.setFixedWidth(270)

        return settings_tab


class PatternSpecificSettings:
    def __init__(self, specific_settings):
        self.specific_settings = specific_settings
    
    def create(self):
        layout = QVBoxLayout()
        layout.addLayout(self.select_channel())
        layout.addStretch(1)
        layout.addWidget(self.period_settings())
        layout.addWidget(self.k_settings())
        layout.addWidget(self.delay_settings())
        layout.addStretch(1)

        return layout

    def select_channel(self):
        channel_label = QLabel('Выбранные каналы')
        self.selected_channel_layout = QGridLayout()
        for i in range(8):
            label = QLabel(str(i))
            label.setAlignment(Qt.AlignCenter)
            self.selected_channel_layout.addWidget(label, 0, i, alignment=Qt.AlignCenter)
            self.selected_channel_layout.addWidget(QCheckBox(), 1, i, alignment=Qt.AlignCenter)
        
        channel_layout = QVBoxLayout()
        channel_layout.addWidget(channel_label)
        channel_layout.addLayout(self.selected_channel_layout)

        return channel_layout

    def period_settings(self):
        period_label = QLabel('Полупериод')
        self.period_input = QSpinBox()
        self.period_input.setValue(1)
        self.period_input.setMinimum(1)
        self.period_input.setMaximum(255)
        self.period_input.setSingleStep(1)
        self.period_input.lineEdit().setValidator(QIntValidator(1, 255, self.specific_settings.main_window))
        self.period_input.valueChanged.connect(self.update_k_input)

        reset_button = QPushButton('Сброс')
        reset_button.clicked.connect(self.reset_period_settings)
        apply_button = QPushButton('Применить')
        apply_button.clicked.connect(self.apply_period_settings)
        button_layout = QHBoxLayout()
        button_layout.addWidget(reset_button)
        button_layout.addWidget(apply_button)

        period_layout = QVBoxLayout()
        period_layout.addWidget(period_label)
        period_layout.addWidget(self.period_input)
        period_layout.addLayout(button_layout)

        period_frame = QFrame(self.specific_settings.main_window)
        period_frame.setLayout(period_layout)
        period_frame.setFrameShape(QFrame.Panel)

        return period_frame

    def reset_period_settings(self):
        pass

    def apply_period_settings(self):
        pass

    def k_settings(self):
        k_label = QLabel('Коэффициент заполнения (%)')
        period = self.period_input.value()*2
        self.k_input = NewQAbstractSpinBox([int(i/period*100) for i in range(period+1) if i/period*100 % 1 == 0])
        self.k_input.lineEdit().setReadOnly(True)

        reset_button = QPushButton('Сброс')
        reset_button.clicked.connect(self.reset_k_settings)
        apply_button = QPushButton('Применить')
        apply_button.clicked.connect(self.apply_k_settings)
        button_layout = QHBoxLayout()
        button_layout.addWidget(reset_button)
        button_layout.addWidget(apply_button)

        k_layout = QVBoxLayout()
        k_layout.addWidget(k_label)
        k_layout.addWidget(self.k_input)
        k_layout.addLayout(button_layout)

        k_frame = QFrame(self.specific_settings.main_window)
        k_frame.setLayout(k_layout)
        k_frame.setFrameShape(QFrame.Panel)

        return k_frame

    def reset_k_settings(self):
        pass

    def apply_k_settings(self):
        pass

    def delay_settings(self):
        delay_label = QLabel('Смещение')
        self.delay_input = QLineEdit()

        reset_button = QPushButton('Сброс')
        reset_button.clicked.connect(self.reset_delay_settings)
        apply_button = QPushButton('Применить')
        apply_button.clicked.connect(self.apply_delay_settings)
        button_layout = QHBoxLayout()
        button_layout.addWidget(reset_button)
        button_layout.addWidget(apply_button)

        delay_layout = QVBoxLayout()
        delay_layout.addWidget(delay_label)
        delay_layout.addWidget(self.delay_input)
        delay_layout.addLayout(button_layout)

        delay_frame = QFrame(self.specific_settings.main_window)
        delay_frame.setLayout(delay_layout)
        delay_frame.setFrameShape(QFrame.Panel)

        return delay_frame

    def reset_delay_settings(self):
        pass

    def apply_delay_settings(self):
        pass

    def update_k_input(self):
        period = self.period_input.value()*2
        self.k_input.update_lst([int(i/period*100) for i in range(period+1) if i/period*100 % 1 == 0])


class UserSpecificSettings:
    def __init__(self, specific_settings):
        self.specific_settings = specific_settings
    
    def create(self):
        user_layout = QVBoxLayout()

        return user_layout
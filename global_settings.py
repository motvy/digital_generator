from customs import NewQAbstractSpinBox

from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame


class GlobalSettings():
    def __init__(self, main_window):
        self.main_window = main_window
    
    def create(self):
        frequency_label = QLabel('Частота (Гц)')
        self.frequency_input = QLineEdit()

        amplitude_label = QLabel('Ампитуда (В)')
        self.amplitude_input = NewQAbstractSpinBox([x / 10.0 for x in range(18, 44, 1)])
        self.amplitude_input.lineEdit().setReadOnly(True)

        length_label = QLabel('Длина')
        self.length_input = QLineEdit()

        reset_button = QPushButton('Сброс')
        reset_button.clicked.connect(self.reset_settings)
        apply_button = QPushButton('Применить')
        apply_button.clicked.connect(self.apply_settings)
        button_layout = QHBoxLayout()
        button_layout.addWidget(reset_button)
        button_layout.addWidget(apply_button)

        settings_layout = QVBoxLayout()
        settings_layout.addWidget(frequency_label)
        settings_layout.addWidget(self.frequency_input)
        settings_layout.addWidget(amplitude_label)
        settings_layout.addWidget(self.amplitude_input)
        settings_layout.addWidget(length_label)
        settings_layout.addWidget(self.length_input)
        settings_layout.addStretch(1)
        settings_layout.addLayout(button_layout)

        settings_frame = QFrame(self.main_window)
        settings_frame.setLayout(settings_layout)
        settings_frame.setFrameShape(QFrame.Panel)
        settings_frame.setFixedWidth(270)
        settings_frame.setFixedHeight(230)

        return settings_frame
    
    def reset_settings(self):
        pass

    def apply_settings(self):
        pass
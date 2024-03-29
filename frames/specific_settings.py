from utils import NewQAbstractSpinBox
import config

from PyQt5.QtGui import QIntValidator, QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QTabWidget, QSpinBox, QCheckBox, QGridLayout
from PyQt5 import sip, QtWidgets


class SpecificSettings():
    def __init__(self, main_window):
        self.main_window = main_window
        self.db = main_window.db

        self.current_mode = 0 # 0 - Pattern settings, 1 - User settings
    
    def create(self):
        self.pattern_settings = PatternSpecificSettings(self, self.db)
        # self.user_settings = UserSpecificSettings(self, self.db)
        self.pattern_layout = self.pattern_settings.create()
        # self.user_layout = self.user_settings.create()

        self.pattern_frame = QFrame(self.main_window)
        self.pattern_frame.setLayout(self.pattern_layout)
        self.pattern_frame.setFrameShape(QFrame.Panel)
        # user_frame = QFrame(self.main_window)
        # user_frame.setLayout(self.user_layout)
        # user_frame.setFrameShape(QFrame.Panel)


        # settings_tab = QTabWidget()
        # settings_tab.addTab(pattern_frame, 'Pattern')
        # settings_tab.addTab(user_frame, 'User')
        # settings_tab.setFixedWidth(270)

        self.pattern_frame.setFixedWidth(270)

        return self.pattern_frame
    
    def new_layout(self, lt):
        self.pattern_frame.setLayout(lt)
    
    def initData(self):
        self.pattern_settings.select_all_channels()
    
    def hasUnsaved(self):

        return self.pattern_settings.has_unsaved()


class PatternSpecificSettings:
    def __init__(self, specific_settings, db):
        self.specific_settings = specific_settings
        self.db = db
        self.selected_channels = []
        self.channels_settings = []
        self.db_settings_dict = {}
    
    def create(self):
        self.layout = QVBoxLayout()
        self.layout.addStretch(1)
        self.layout.addLayout(self.select_channel())
        self.layout.addStretch(1)
        self.layout.addWidget(self.period_settings())
        self.layout.addWidget(self.k_settings())
        self.layout.addWidget(self.delay_settings())
        self.layout.addStretch(1)
        self.layout.addWidget(self.operation_mode_button())

        self.initData()
        self.specific_settings.current_mode = 0
        self.specific_settings.main_window.regenerate_plot()
        return self.layout

    def operation_mode_button(self):
        mode_button = QPushButton("В режим ручного задания параметров")
        mode_button.clicked.connect(lambda: self.deleteLayout(self.layout, UserSpecificSettings(self.specific_settings, self.db).create()))
        # mode_button.setStyleSheet("QPushButton {background-color: #f0f0f0; border: 0px;}")
        # mode_button.setFixedHeight(30)
        return mode_button

    def deleteLayout(self, layout, new_lt):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.deleteLayout(item.layout(), new_lt)
            sip.delete(layout)

        self.specific_settings.new_layout(new_lt)

    def select_channel(self):
        channel_label = QLabel('Выбранные каналы')
        self.select_all_channels_cb = QCheckBox()
        self.select_all_channels_cb.clicked.connect(lambda: self.select_all_channels())

        channel_label_layout = QHBoxLayout()
        channel_label_layout.addWidget(self.select_all_channels_cb)
        channel_label_layout.addWidget(channel_label)
        channel_label_layout.addStretch()

        self.selected_channel_layout = QGridLayout()
        for i in range(8):
            label = QLabel(str(i))
            label.setAlignment(Qt.AlignCenter)
            self.selected_channel_layout.addWidget(label, 0, i, alignment=Qt.AlignCenter)

            channel_cb = QCheckBox()
            channel_cb.clicked.connect(lambda: self.selected_channels_changed())
            self.selected_channel_layout.addWidget(channel_cb, 1, i, alignment=Qt.AlignCenter)

        channel_layout = QVBoxLayout()
        channel_layout.addLayout(channel_label_layout)
        channel_layout.addLayout(self.selected_channel_layout)

        return channel_layout

    def selected_channels_changed(self):
        """
        Зависимости:
        Задержка < Длина
        Полупериод < Длина
        1) get_selected_channels -> [int]
        2) change period - change k
        3) change k
        4) change delay
        """
        # self.selected_channels = self.get_selected_channels()
        self.initData()

    def get_selected_channels(self):
        channels = []
        for i in range(self.selected_channel_layout.columnCount()):
            cb = self.selected_channel_layout.itemAtPosition(1, i).widget()
            if cb.isChecked():
                channels.append(i)

        checked_all = True if len(channels) == self.selected_channel_layout.columnCount() else False
        self.select_all_channels_cb.setChecked(checked_all)

        return channels

    def select_all_channels(self):
        checked = False if len(self.get_selected_channels()) == self.selected_channel_layout.columnCount() else True
        for i in range(self.selected_channel_layout.columnCount()):
            self.selected_channel_layout.itemAtPosition(1, i).widget().setChecked(checked)
        
        self.select_all_channels_cb.setChecked(checked)
        self.selected_channels_changed()

    def change_global_length(self):
        global_length = self.db.get_global_settings().length

        period = self.period_input.text()
        if period and int(period) > global_length // 2:
            self.period_input.setText(str(global_length // 2))
            self.apply_period_settings()

        delay = self.delay_input.text()
        if delay and int(delay) > global_length - 1:
            self.delay_input.setText(str(global_length - 1))
            self.apply_delay_settings()
        
        # for i in range(8):
        #     settings = self.db.get_specific_pattern_settings()
        #     period = settings.period
        #     delay = settings.delay


    def period_settings(self):
        self.period_label = QLabel('Полупериод')
        self.period_input = QLineEdit()
        self.period_input.textChanged.connect(lambda: self.change_period())

        reset_button = QPushButton('По умолчанию')
        reset_button.clicked.connect(lambda: self.reset_period_settings())
        apply_button = QPushButton('Применить')
        apply_button.clicked.connect(lambda: self.apply_period_settings())
        button_layout = QHBoxLayout()
        button_layout.addWidget(reset_button)
        button_layout.addWidget(apply_button)

        period_layout = QVBoxLayout()
        period_layout.addWidget(self.period_label)
        period_layout.addWidget(self.period_input)
        period_layout.addLayout(button_layout)

        self.period_frame = QFrame(self.specific_settings.main_window)
        self.period_frame.setLayout(period_layout)
        self.period_frame.setFrameShape(QFrame.Panel)

        return self.period_frame

    def reset_period_settings(self):
        self.period_input.setText(str(config.DEFAULT_SPECIFIC_PATTERN_SETTINGS['period']))
        self.apply_period_settings()

    def apply_period_settings(self):
        global_length = self.db.get_global_settings().length
        period = self.period_input.text()

        if not period or int(period) < config.DEFAULT_SPECIFIC_PATTERN_SETTINGS['period']:
            period = config.DEFAULT_SPECIFIC_PATTERN_SETTINGS['period']
        elif int(period) > global_length // 2:
            period = global_length // 2
        else:
            period = int(period)

        self.period_input.setText(str(period))
        if period and period != self.db_settings_dict['period']:
            period = int(period)

            self.db_settings_dict['period'] = period
            self.period_label.setText(self.period_label.text().strip('*'))
            for ch in self.selected_channels:
                self.db.set_specific_pattern_period(ch, period)
            self.channels_settings = [self.db.get_specific_pattern_settings(ch) for ch in self.selected_channels]

        self.update_k_input()

        self.specific_settings.main_window.regenerate_plot()

    def update_period_input(self):
        if len(set([ch.period for ch in self.channels_settings])) == 1:
            self.period_input.setText(str(self.channels_settings[0].period))
            self.db_settings_dict['period'] = self.channels_settings[0].period
            self.k_frame.setEnabled(True)
            self.apply_period_settings()
        else:
            self.period_input.clear()
            self.k_input.lineEdit().clear()
            self.k_frame.setEnabled(False)
    
    def change_period(self):
        if 'period' not in self.db_settings_dict:
            return
        
        if not self.period_input.text() or int(self.period_input.text()) != self.db_settings_dict['period']:
            self.period_label.setText(self.period_label.text().strip('*') + '*')
        else:
            self.period_label.setText(self.period_label.text().strip('*'))

    def k_settings(self):
        self.k_label = QLabel('Коэффициент заполнения (%)')
        self.k_input = NewQAbstractSpinBox()
        self.k_input.lineEdit().setReadOnly(True)
        self.k_input.lineEdit().textChanged.connect(lambda: self.change_k())

        reset_button = QPushButton('По умолчанию')
        reset_button.clicked.connect(lambda: self.reset_k_settings())
        apply_button = QPushButton('Применить')
        apply_button.clicked.connect(lambda: self.apply_k_settings())
        button_layout = QHBoxLayout()
        button_layout.addWidget(reset_button)
        button_layout.addWidget(apply_button)

        k_layout = QVBoxLayout()
        k_layout.addWidget(self.k_label)
        k_layout.addWidget(self.k_input)
        k_layout.addLayout(button_layout) 

        self.k_frame = QFrame(self.specific_settings.main_window)
        self.k_frame.setLayout(k_layout)
        self.k_frame.setFrameShape(QFrame.Panel)

        return self.k_frame

    def reset_k_settings(self):
        self.k_input.setValue(config.DEFAULT_SPECIFIC_PATTERN_SETTINGS['k'])
        self.apply_k_settings()

    def apply_k_settings(self):
        k = int(self.k_input.value())
        if k != self.db_settings_dict.get('k', None):
            self.db_settings_dict['k'] = k
            self.k_label.setText(self.k_label.text().strip('*'))
            for ch in self.selected_channels:
                self.db.set_specific_pattern_k(ch, k)
            self.channels_settings = [self.db.get_specific_pattern_settings(ch) for ch in self.selected_channels]
        
        self.specific_settings.main_window.regenerate_plot()

    def change_k(self):
        if not self.k_input.lineEdit().text():
            return
        
        if int(self.k_input.value()) != self.db_settings_dict.get('k', None):
            self.k_label.setText(self.k_label.text().strip('*') + '*')
        else:
            self.k_label.setText(self.k_label.text().strip('*'))

    def update_k_input(self):
        if not self.period_input.text():
            self.k_input.lineEdit().clear()
            self.k_frame.setEnabled(False)
            return
        else:
            self.k_frame.setEnabled(True)

        period = int(self.period_input.text()) * 2

        k_values = [int(i/period*100) for i in range(period+1) if i/period*100 % 1 == 0]
        self.k_input.setRange(k_values)
        if len(set([ch.k for ch in self.channels_settings])) == 1:
            if self.channels_settings[0].k in k_values:
                self.k_input.setValue(self.channels_settings[0].k)
                self.apply_k_settings()
            elif self.k_input.value() and int(self.k_input.value()) in k_values:
                pass
            else:
                self.k_input.setValue(config.DEFAULT_SPECIFIC_PATTERN_SETTINGS['k'])
                self.apply_k_settings()
        else:
            self.k_input.lineEdit().clear()

    def delay_settings(self):
        self.delay_label = QLabel('Смещение')
        self.delay_input = QLineEdit()
        self.delay_input.textChanged.connect(lambda: self.change_delay())

        reset_button = QPushButton('По умолчанию')
        reset_button.clicked.connect(lambda: self.reset_delay_settings())
        apply_button = QPushButton('Применить')
        apply_button.clicked.connect(lambda: self.apply_delay_settings())
        button_layout = QHBoxLayout()
        button_layout.addWidget(reset_button)
        button_layout.addWidget(apply_button)

        delay_layout = QVBoxLayout()
        delay_layout.addWidget(self.delay_label)
        delay_layout.addWidget(self.delay_input)
        delay_layout.addLayout(button_layout)

        self.delay_frame = QFrame(self.specific_settings.main_window)
        self.delay_frame.setLayout(delay_layout)
        self.delay_frame.setFrameShape(QFrame.Panel)

        return self.delay_frame

    def reset_delay_settings(self):
        self.delay_input.setText(str(config.DEFAULT_SPECIFIC_PATTERN_SETTINGS['delay']))
        self.apply_delay_settings()

    def apply_delay_settings(self):
        delay = self.delay_input.text()
        global_length = self.db.get_global_settings().length

        if not delay or int(delay) < config.DEFAULT_SPECIFIC_PATTERN_SETTINGS['delay']:
            delay = config.DEFAULT_SPECIFIC_PATTERN_SETTINGS['delay']
        elif int(delay) > global_length - 1:
            delay = global_length - 1
        else:
            delay = int(delay)

        self.delay_input.setText(str(delay))
        if delay != self.db_settings_dict['delay']:
            delay = int(delay)

            self.db_settings_dict['delay'] = delay
            self.delay_label.setText(self.delay_label.text().strip('*'))
            for ch in self.selected_channels:
                self.db.set_specific_pattern_delay(ch, delay)
            self.channels_settings = [self.db.get_specific_pattern_settings(ch) for ch in self.selected_channels]
        
        self.specific_settings.main_window.regenerate_plot()

    def change_delay(self):
        if 'delay' not in self.db_settings_dict:
            return
        
        if not self.delay_input.text() or int(self.delay_input.text()) != self.db_settings_dict['delay']:
            self.delay_label.setText(self.delay_label.text().strip('*') + '*')
        else:
            self.delay_label.setText(self.delay_label.text().strip('*'))

    def update_delay_input(self):
        self.delay_input.setValidator(QIntValidator(0, 255, self.specific_settings.main_window))
        if len(set([ch.delay for ch in self.channels_settings])) == 1:
            self.db_settings_dict['delay'] = self.channels_settings[0].delay
            self.delay_input.setText(str(self.channels_settings[0].delay))
            self.apply_delay_settings()
        else:
            self.delay_input.clear()

    def initData(self):
        self.specific_settings.pattern_settings = self
        self.selected_channels = self.get_selected_channels()
        self.channels_settings = [self.db.get_specific_pattern_settings(ch) for ch in self.selected_channels]

        if len(self.selected_channels) == 0:
            self.delay_frame.setEnabled(False)
            self.period_frame.setEnabled(False)
            self.k_frame.setEnabled(False)
            self.delay_input.clear()
            self.delay_label.setText(self.delay_label.text().strip('*'))
            self.period_input.clear()
            self.period_label.setText(self.period_label.text().strip('*'))
            self.k_input.lineEdit().clear()
        else:
            self.delay_frame.setEnabled(True)
            self.period_frame.setEnabled(True)

            self.update_period_input()
            if 'period' not in self.db_settings_dict:
                self.db_settings_dict['period'] = None
            self.period_label.setText(self.period_label.text().strip('*'))

            self.update_delay_input()
            if 'delay' not in self.db_settings_dict:
                self.db_settings_dict['delay'] = None
            self.delay_label.setText(self.delay_label.text().strip('*'))

            self.update_k_input()
    
    def has_unsaved(self):
        for label in (self.delay_label, self.period_label, self.k_label):
            if '*' in label.text():
                return True
        return False
            

class UserSpecificSettings:
    def __init__(self, specific_settings, db):
        self.specific_settings = specific_settings
        self.db = db
        self.db_settings = []
        self.channels_settings = []
    
    def create(self):
        reset_button = QPushButton('По умолчанию')
        reset_button.clicked.connect(lambda: self.reset_settings())
        apply_button = QPushButton('Применить')
        apply_button.clicked.connect(lambda: self.apply_settings())
        button_layout = QHBoxLayout()
        button_layout.addWidget(reset_button)
        button_layout.addWidget(apply_button)


        self.layout = QVBoxLayout()
        self.layout.addLayout(self.get_channels())
        self.layout.addStretch()
        self.layout.addLayout(button_layout)
        self.layout.addWidget(self.operation_mode_button())

        self.initData()
        self.specific_settings.current_mode = 1
        self.specific_settings.main_window.regenerate_plot()

        return self.layout

    def reset_settings(self):
        for indx in  range(8):
            self.db.set_specific_user_value(indx, config.DEFAULT_SPECIFIC_USER_SETTINGS['value'])
        
        self.initData()

    def apply_settings(self):
        for indx in  range(self.channels_layout.count()):
            item_lt = self.channels_layout.itemAtPosition(indx, 0)
            item_le = item_lt.itemAtPosition(1, 0).itemAtPosition(0, 1).widget()
            le_text = item_le.text().upper()

            if set(item_le.text()) - {'1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'A', 'B', 'C', 'D', 'E', 'F'}:
                le_text = config.DEFAULT_SPECIFIC_USER_SETTINGS['value']

            self.db_settings[indx] = le_text
            self.db.set_specific_user_value(indx, le_text)
            item_le.setText(le_text)
            lb = item_lt.itemAtPosition(0, 0).widget()
            lb.setText(lb.text().strip('*'))
        
        self.specific_settings.main_window.regenerate_plot()

    def initData(self):
        self.specific_settings.pattern_settings = self
        self.channels_settings = [self.db.get_specific_user_settings(ch) for ch in range(8)]
        self.db_settings = self.channels_settings

        for indx in  range(self.channels_layout.count()):
            item_lt = self.channels_layout.itemAtPosition(indx, 0)
            item_le = item_lt.itemAtPosition(1, 0).itemAtPosition(0, 1).widget()
            item_le.setText(self.channels_settings[indx])

    def get_channels(self):

        self.channels_layout = QGridLayout()

        for i in range(8):
            plot_le = QLineEdit()
            plot_le.textChanged.connect(lambda: self.change_val())
            plot_le.setMaxLength(32)

            phl = QGridLayout()
            phl.addWidget(QLabel("0x"), 0, 0)
            phl.addWidget(plot_le, 0, 1)
            # plot_le.setCursorPosition(3)
            # plot_le.setReadOnly(1);
            # plot_cb.clicked.connect(lambda: self.set_channel_enabled())
            # plot_cb.setChecked(True)

            plot_label = QLabel("Канал " + str(i))
            # plot_label.setStyleSheet('font-size: 10pt;')
            # plot_label.setDisabled(True)
            curr = QGridLayout() 
            curr.addWidget(plot_label, 0, 0)
            curr.addLayout(phl, 1, 0)

            self.channels_layout.addLayout(curr, i, 0)

        return self.channels_layout

    def change_val(self):
        item = self.specific_settings.main_window.sender()

        for indx in  range(self.channels_layout.count()):
            item_lt = self.channels_layout.itemAtPosition(indx, 0)
            item_le = item_lt.itemAtPosition(1, 0).itemAtPosition(0, 1).widget()
            if item == item_le:
                lb = item_lt.itemAtPosition(0, 0).widget()
                if item_le.text() != self.db_settings[indx]:
                    lb.setText(lb.text().strip('*') + '*')
                else:
                    lb.setText(lb.text().strip('*'))
                break
        # if int(self.k_input.value()) != self.db_settings_dict.get('k', None):
        #     self.k_label.setText(self.k_label.text().strip('*') + '*')
        # else:
        #     self.k_label.setText(self.k_label.text().strip('*'))
        # pass

    def operation_mode_button(self):
        mode_button = QPushButton("В режим автоматичского задания параметров")
        mode_button.clicked.connect(lambda: self.deleteLayout(self.layout, PatternSpecificSettings(self.specific_settings, self.db).create()))
        # mode_button.setStyleSheet("QPushButton {background-color: #f0f0f0; border: 0px;}")
        # mode_button.setFixedHeight(30)
        return mode_button

    def deleteLayout(self, layout, new_lt):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.deleteLayout(item.layout(), new_lt)
            sip.delete(layout)

        self.specific_settings.new_layout(new_lt)

    def has_unsaved(self):
        for indx in  range(self.channels_layout.count()):
            item_lt = self.channels_layout.itemAtPosition(indx, 0)
            lb = item_lt.itemAtPosition(0, 0).widget()
            if '*' in lb.text():
                return True

        return False

from collections import namedtuple

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QAbstractSpinBox
import pyqtgraph as pg

GlobalSettings = namedtuple('GlobalSettings', 'frequency, amplitude, length, frequency_source')
SpecificPatternSettings = namedtuple('SpecificPatternSettings', 'period, k, delay')

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

class NewQAbstractSpinBox(QAbstractSpinBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lst = []
        self.indx= 0
        self.lineEdit().setText('')

    def stepEnabled(self):
        if self.indx == 0:
            return QAbstractSpinBox.StepUpEnabled
        elif self.indx == len(self.lst)-1:
            return QAbstractSpinBox.StepDownEnabled
        else:
            return QAbstractSpinBox.StepUpEnabled | QAbstractSpinBox.StepDownEnabled

    def stepBy(self, p_int):
        num = self.indx + p_int
        if num < len(self.lst):
            self.indx = num
            self.lineEdit().setText(str(self.lst[self.indx]))
        else:
            pass

    def setRange(self, lst):
        self.lst = lst
        self.indx = 0
        # self.lineEdit().setText(str(lst[self.indx]))
    
    def value(self):
        return self.lst[self.indx] if self.lst else None

    def setValue(self, value):
        self.indx = self.lst.index(value) if value in self.lst else 0
        self.lineEdit().setText(str(self.lst[self.indx]))

class MyPlotWidget(pg.PlotWidget):
    clicked = pyqtSignal()
    def mouseReleaseEvent(self, QMouseEvent):
        if QMouseEvent.button()==Qt.LeftButton:
            self.clicked.emit()

from PyQt5.QtWidgets import QAbstractSpinBox


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

QGridLayout:gridcell(0,1) 
{
    border: 10px solid black;
    margin: 0px;
}
"""

class NewQAbstractSpinBox(QAbstractSpinBox):
    def __init__(self, lst, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lst = lst
        self.indx = 0
        self.lineEdit().setText(str(lst[self.indx]))

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
    
    def update_lst(self, lst):
        self.lst = lst
        self.indx = 0
        self.lineEdit().setText(str(lst[self.indx]))
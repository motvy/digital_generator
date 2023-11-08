from frames import main_window

from PyQt5.QtWidgets import QApplication

import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

app = QApplication(sys.argv)

window = main_window.MainWindow()
window.show()

app.exec()
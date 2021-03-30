import sys
from PySide2 import QtWidgets
from ui import DashboardUi
from ui import WeatherWidget

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    db = DashboardUi()
    db.showMaximized()
    db.show()
    app.exec_()

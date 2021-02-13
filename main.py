import sys
from PySide2 import QtWidgets
from ui import DashboardUi
from ui import WeatherWidget
# import cProfile
#
# pr = cProfile.Profile()
# pr.enable()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    db = DashboardUi()
    db.showMaximized()
    db.show()
    # wv = WeatherWidget()
    # wv.show()
    app.exec_()
    # pr.dump_stats(r'C:\Users\antoi\Desktop\prof.pstats')




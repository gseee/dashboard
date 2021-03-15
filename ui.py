from PySide2 import QtWidgets, QtCore, QtGui
import datetime
import requests
import webbrowser
import weather
import hdd
import read_email
import steam
import reddit
import loading_icon
import functools


class WeatherWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__thread = None
        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.load = loading_icon.LoadingIcon()
        self.refresh()

    def refresh(self):
        self.main_layout.addWidget(self.load)
        self.load.start()
        self.__thread = GetDataThread(weather.get_data_weather)
        self.__thread.data_received.connect(self._refresh)
        self.__thread.start()

    def _refresh(self, data_list):
        self.load.stop()
        self.main_layout.removeWidget(self.load)

        for n in data_list:
            layout = QtWidgets.QVBoxLayout()
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(n.icon)
            label = QtWidgets.QLabel()
            label.setPixmap(pixmap)
            label_temp = QtWidgets.QLabel()
            label_temp.setText(n.week_day + ', ' + str(round(n.temperature)) + '°C')
            [layout.addWidget(w) for w in (label, label_temp)]
            self.main_layout.addLayout(layout)
            self.main_layout.setSpacing(0)


class SteamNewsWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.load = loading_icon.LoadingIcon()
        self.__thread = None
        self.refresh()

    def refresh(self):
        self.main_layout.addWidget(self.load)
        self.load.start()
        self.__thread = GetDataThread(steam.get_steam_news)
        self.__thread.data_received.connect(self._refresh)
        self.__thread.start()

    def _refresh(self, data_list):
        self.load.stop()
        self.main_layout.removeWidget(self.load)

        for n in data_list:
            layout = QtWidgets.QHBoxLayout()
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(n.header)
            steam_icon = QtWidgets.QLabel()
            steam_icon.setPixmap(pixmap)
            pushbutton = QtWidgets.QPushButton(n.title)
            pushbutton.clicked.connect(functools.partial(webbrowser.open, n.url))
            pushbutton.setStyleSheet(style_button)
            date = QtWidgets.QLabel()
            date.setText(n.date)
            [layout.addWidget(w) for w in (steam_icon, pushbutton, date)]
            layout.setSpacing(0)
            self.main_layout.addLayout(layout)
            self.main_layout.setSpacing(0)


class SteamFriendWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__thread = None
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.load = loading_icon.LoadingIcon()
        self.refresh()

    def refresh(self):
        self.main_layout.addWidget(self.load)
        self.load.start()
        self.__thread = GetDataThread(steam.get_steam_friends)
        self.__thread.data_received.connect(self._refresh)
        self.__thread.start()

    def _refresh(self, data_list):
        self.load.stop()
        self.main_layout.removeWidget(self.load)

        for n in data_list:
            layout = QtWidgets.QHBoxLayout()
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(n.avatar)
            steam_avatar = QtWidgets.QLabel()
            steam_avatar.setPixmap(pixmap)
            pushbutton = QtWidgets.QPushButton(n.personaname)
            pushbutton.clicked.connect(functools.partial(webbrowser.open, n.profileurl))
            pushbutton.setStyleSheet(style_button)
            [layout.addWidget(w) for w in (steam_avatar, pushbutton)]
            layout.setSpacing(0)
            self.main_layout.addLayout(layout)
            self.main_layout.setSpacing(0)


class RedditFrNewsWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__thread = None
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.load = loading_icon.LoadingIcon()
        self.refresh()

    def refresh(self):
        self.main_layout.addWidget(self.load)
        self.load.start()
        self.__thread = GetDataThread(reddit.reddit_french_sub)
        self.__thread.data_received.connect(self._refresh)
        self.__thread.start()

    def _refresh(self, data_list):
        self.load.stop()
        self.main_layout.removeWidget(self.load)

        for n in data_list:
            layout = QtWidgets.QHBoxLayout()
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(n.thumbnail)
            reddit_icon = QtWidgets.QLabel()
            reddit_icon.setPixmap(pixmap)
            pushbutton = QtWidgets.QPushButton(n.title)
            pushbutton.clicked.connect(functools.partial(webbrowser.open, n.shortlink))
            pushbutton.setStyleSheet(style_button)
            [layout.addWidget(w) for w in (reddit_icon, pushbutton)]
            layout.setSpacing(0)
            self.main_layout.addLayout(layout)
            self.main_layout.setSpacing(0)


class GetDataThread(QtCore.QThread):
    data_received = QtCore.Signal(list)

    def __init__(self, get_data_func, *args, **kwargs):
        super().__init__()
        self.__func = get_data_func
        self.__func_args = args
        self.__func_kwargs = kwargs

    def run(self):
        data = self.__func(*self.__func_args, **self.__func_kwargs)
        self.data_received.emit(data)


class DashboardUi(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Dashboard')
        self.setStyleSheet("background-color: #c5d5e2;")
        self.setup_ui()

    def setup_ui(self):
        self.__create_widgets()
        self.__create_layouts()
        self.__modify_widgets()
        self.__add_widgets_to_layouts()
        self.__setup_connections()

    def __create_widgets(self):
        self.name_title_lbl = QtWidgets.QLabel('   Dashboard')
        self.date_title_lbl = QtWidgets.QLabel(datetime.datetime.now().strftime("%A, %d-%m-%y   "))
        self.weather_title_lbl = QtWidgets.QLabel('Weather ' + requests.get('http://ipinfo.io/city').text)
        self.weather_widget = WeatherWidget()
        self.hdd_title_lbl = QtWidgets.QLabel('Hard Drive Capacity')
        self.email_lbl = QtWidgets.QLabel('Last Email')
        self.reddit_news_lbl = QtWidgets.QLabel('Reddit France')
        self.reddit_widget = RedditFrNewsWidget()
        self.steam_news_title_lbl = QtWidgets.QLabel('Steam News')
        self.steam_news_widget = SteamNewsWidget()
        self.steam_friends_title_lbl = QtWidgets.QLabel('Steam Friends')
        self.steam_friends_widget = SteamFriendWidget()

    def __create_layouts(self):
        self.main_layout = QtWidgets.QGridLayout(self)
        self.title_layout = QtWidgets.QHBoxLayout()
        self.weather_layout = QtWidgets.QVBoxLayout()
        self.hdd_layout = QtWidgets.QVBoxLayout()
        self.email_layout = QtWidgets.QVBoxLayout()
        self.reddit_layout = QtWidgets.QVBoxLayout()
        self.steam_news_layout = QtWidgets.QVBoxLayout()
        self.steam_friends_layout = QtWidgets.QVBoxLayout()

    def __modify_widgets(self):
        self.title_layout.setSpacing(0)

        self.name_title_lbl.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.date_title_lbl.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.name_title_lbl.setStyleSheet(style_top_title)
        self.date_title_lbl.setStyleSheet(style_top_title)
        self.name_title_lbl.setFixedHeight(60)
        self.date_title_lbl.setFixedHeight(60)

        self.weather_title_lbl.setStyleSheet(style_title)
        self.weather_title_lbl.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.weather_title_lbl.setFixedHeight(20)

        self.hdd_title_lbl.setStyleSheet(style_title)
        self.hdd_title_lbl.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.hdd_title_lbl.setFixedHeight(40)

        self.reddit_news_lbl.setStyleSheet(style_title)
        self.reddit_news_lbl.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.reddit_news_lbl.setFixedHeight(40)

        self.email_lbl.setStyleSheet(style_title)
        self.email_lbl.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.email_lbl.setFixedHeight(40)


        self.steam_news_title_lbl.setStyleSheet(style_title)
        self.steam_news_title_lbl.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.steam_news_title_lbl.setFixedHeight(40)

        self.steam_friends_title_lbl.setStyleSheet(style_title)
        self.steam_friends_title_lbl.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.steam_friends_title_lbl.setFixedHeight(40)

    def __add_widgets_to_layouts(self):
        [self.title_layout.addWidget(w) for w in (self.name_title_lbl, self.date_title_lbl)]
        [self.weather_layout.addWidget(w) for w in (self.weather_title_lbl, self.weather_widget)]
        [self.reddit_layout.addWidget(w) for w in (self.reddit_news_lbl, self.reddit_widget)]
        self.hdd_layout.addWidget(self.hdd_title_lbl)
        self.email_layout.addWidget(self.email_lbl)
        [self.steam_news_layout.addWidget(w) for w in (self.steam_news_title_lbl, self.steam_news_widget)]
        [self.steam_friends_layout.addWidget(w) for w in (self.steam_friends_title_lbl, self.steam_friends_widget)]

        self.main_layout.addLayout(self.title_layout, 0, 0, 1, 3)
        self.main_layout.addLayout(self.weather_layout, 1, 0, 1, 3)
        self.main_layout.addLayout(self.hdd_layout, 2, 0, 1, 1)
        self.main_layout.addLayout(self.email_layout, 2, 1, 1, 1)
        self.main_layout.addLayout(self.reddit_layout, 3, 0, 1, 1)
        self.main_layout.addLayout(self.steam_news_layout, 2, 2, 1, 1)
        self.main_layout.addLayout(self.steam_friends_layout, 3, 2, 1, 1)

    def __setup_connections(self):
        self.set_hdd()
        self.set_email()

    def set_hdd(self):
        hdd_data = hdd.get_hdd_data()
        for h in range(len(hdd_data)):
            layout = QtWidgets.QHBoxLayout()
            name_hdd = QtWidgets.QLabel(str(hdd_data[0][h]))
            progress_bar = QtWidgets.QProgressBar()
            progress_bar.setMinimum(0)
            progress_bar.setMaximum(100)
            progress_bar.setValue(hdd_data[1][h][3])
            giga_hdd_lbl = QtWidgets.QLabel(str(hdd_data[1][h][1]) + ' / ' + str(hdd_data[1][h][0]))
            [layout.addWidget(w) for w in (name_hdd, progress_bar, giga_hdd_lbl)]
            self.hdd_layout.addLayout(layout)

    def set_email(self):
        email = read_email.read_email()
        for e in email:
            layout = QtWidgets.QHBoxLayout()
            date_email = QtWidgets.QLabel(e.date)
            sender_email = QtWidgets.QLabel(e.sender)
            subject_email = QtWidgets.QLabel(e.subject)
            [layout.addWidget(w) for w in(date_email, sender_email, subject_email)]
            self.email_layout.addLayout(layout)



style_top_title = '''QLabel { background-color: #1b2838; color: white; font: Verdana;
font-size: 30px; border: 0px
}'''

style_title = '''QLabel { background-color: #1b2838; color: white; font: Verdana;
font-size: 10px; border: 0px; height: 60px;
}'''

style_other = '''QLabel { background-color: #1b2838; color: white; font: Verdana;
font-size: 12px; border: 0px
}'''

style_button = '''QPushButton, QLabel { background-color: black ; color: white; 
font: Verdana; border: none; margin: 0px; padding: 0px;
}'''

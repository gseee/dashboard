import requests
import datetime
from collections import namedtuple
from config import WEATHER_API


WeatherData = namedtuple('WeatherData', "week_day temperature icon")


def get_data_weather():

    info_loc = (requests.get('http://ipinfo.io/loc')).text[0:-1].split(',')
    weather_data = requests.get(
        'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&units=metric&appid={}'.format(info_loc[0],
                                                                                                     info_loc[1],
                                                                                                     WEATHER_API)).json()
    week_data = weather_data['daily']
    week_data_list = []

    for daily in week_data:
        week_date = datetime.datetime.utcfromtimestamp(daily['dt']).strftime('%a')
        weather_icon = requests.get('http://openweathermap.org/img/wn/' + daily['weather'][0]['icon'] + '@2x.png').content
        week_data_list.append(WeatherData(week_date, daily['temp']['day'], weather_icon))

    return week_data_list

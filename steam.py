import requests
import datetime
from collections import namedtuple
from multiprocessing.pool import ThreadPool
from config import STEAM_API, STEAM_USER_ID

SteamNewsData = namedtuple('SteamNewsData', "title url date header date_time")
SteamFriendData = namedtuple('SteamFriendData', "steamid personaname profileurl avatar")


def __get_steam_friends_threading(friend_url):
    user_friend_data = []
    request = requests.get(friend_url).json()

    if not request['response']['players'][0]['personastate'] == 0:
        request_data = request['response']['players'][0]
        avatar = requests.get(request_data['avatar']).content

        user_friend_data.append(SteamFriendData(request_data['steamid'], request_data['personaname'],
                                                request_data['profileurl'], avatar))

    return user_friend_data


def __get_steam_news_treading(tuple_arg):
    url, limit_date = tuple_arg
    news_games = []
    news = requests.get(url).json()

    for new in news['appnews']['newsitems']:
        if datetime.datetime.utcfromtimestamp(new['date']) < limit_date:
            continue

        header = requests.get(
            'http://cdn.akamai.steamstatic.com/steam/apps/{}/header.jpg'.format(new['appid'])).content
        date = datetime.datetime.utcfromtimestamp(new['date']).strftime('%d %b')
        news_games.append(SteamNewsData(new['title'], new['url'], date, header, new['date']))

    return news_games


def get_steam_news():
    list_games = []
    today = datetime.datetime.now()
    two_mouth = today - datetime.timedelta(weeks=12)

    user_games = requests.get(
        'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={}&steamid={}'.format(STEAM_API,
                                                                                                   STEAM_USER_ID)).json()
    for games in user_games['response']['games']:
        if not games['appid'] and games['playtime_forever'] < 120:
            continue
        list_games.append(games['appid'])

    list_url = []
    news_games = []

    for appid in list_games:
        url = 'http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid={}&count=3&maxlength=300&format=json'.format(
            appid)
        list_url.append(url)

    with ThreadPool(50) as tp:
        list_news_games = tp.map(__get_steam_news_treading, [(url, two_mouth) for url in list_url])

    for game in list_news_games:
        news_games += game

    news_games.sort(key=lambda steam_news_data: steam_news_data.date_time, reverse=True)
    news_games = news_games[:5]

    return news_games


def get_steam_friends():
    user_friend = requests.get(
        'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={}&steamid={}&relationship=friend'.format(
            STEAM_API,
            STEAM_USER_ID)).json()

    user_friend_data = []
    list_url = []

    for friend in user_friend['friendslist']['friends']:
        list_url.append(
            'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={}&steamids={}'.format(STEAM_API,
                                                                                                         friend[
                                                                                                             'steamid']))

    with ThreadPool(50) as tp:
        user_friend = tp.map(__get_steam_friends_threading, list_url)

    for friend in user_friend:
        user_friend_data += friend

    return user_friend_data

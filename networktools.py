from time import sleep_ms, time


def connect_to_network():
    """connects to Wi-Fi"""
    from secrets import secrets
    from network import WLAN, STA_IF
    ssid = secrets['SSID']
    password = secrets['PASSWORD']
    # initialize wlan object
    wlan = WLAN(STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    # try to connect for 10 times with waiting time of one second
    for i in range(1, 10):
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        print('waiting for connection...')
        sleep_ms(1000)
    if wlan.status() != 3:
        from quicktools import logger
        logger('Network connection failed\n')
        del logger
        raise RuntimeError('network connection failed')
    else:
        print('connected')
        status = wlan.ifconfig()
        print('ip = ' + status[0])
    del WLAN, STA_IF, secrets


def get_free_games_names_from_epic():
    from urequests import get

    url = 'https://store-site-backend-static.ak.epicgames.com/freeG' \
          'amesPromotions?locale=en-US&country=PL&allowCountries=PL'
    source_str = str(get(url).text)

    games = {}
    while True:
        game_name_end_ind = source_str.find('","id')

        if game_name_end_ind == -1:
            break

        game_name_start_ind = source_str[:game_name_end_ind].rfind('"') + 1
        game_name = source_str[game_name_start_ind:game_name_end_ind]

        start_date_end_ind = source_str[game_name_end_ind:].find('","endDate')
        start_date_start_ind = source_str[game_name_end_ind:][:start_date_end_ind].rfind('"') + 1
        start_date = source_str[game_name_end_ind:][start_date_start_ind:start_date_end_ind]

        end_date_end_ind = source_str[game_name_end_ind:].find('","discountSetting')
        end_date_start_ind = source_str[game_name_end_ind:][:end_date_end_ind].rfind('"') + 1
        end_date = source_str[game_name_end_ind:][end_date_start_ind:end_date_end_ind]

        source_str = source_str[game_name_end_ind:][end_date_end_ind + 18:]

        games.update({game_name: {'START_DATE': start_date[:-8], 'END_DATE': end_date[:-8]}})
    del get
    return games


def get_external_data():
    from urequests import get
    from secrets import secrets
    print("downloading external data")
    apikey = secrets['API_KEY']
    success = 0
    ext_data = {}
    while success == 0:
        try:
            ip = get('http://api.ipify.org').text
            sleep_ms(10)
            latlong = str(get(f'http://ipapi.co/{ip}/latlong/').text).split(",")
            sleep_ms(10)
            req = get(
                f"https://api.openweathermap.org/data/2.5/weather?lat={latlong[0]}&lon={latlong[1]}&appid={apikey}").text

            import ujson
            external_data = dict(ujson.loads(req))

            external_data.pop('visibility')
            external_data.pop('id')
            external_data.pop('coord')
            external_data.pop('cod')
            external_data.pop('dt')
            external_data.pop('wind')

            external_data['sunrise'] = external_data['sys']['sunrise']
            external_data['sunset'] = external_data['sys']['sunset']
            external_data['location'] = f"{external_data['sys']['country']} {external_data['name']}"
            external_data['pressure'] = external_data['main']['pressure']
            external_data['real feel temperature'] = external_data['main']['feels_like'] - 273.15
            external_data['humidity'] = external_data['main']['humidity']
            external_data['real temperature'] = external_data['main']['temp'] - 273.15
            external_data['cloud coverage'] = external_data['clouds']['all']
            external_data['weather icon'] = external_data['weather'][0]['icon']
            external_data['weather'] = external_data['weather'][0]['description']

            external_data.pop('name')
            external_data.pop('sys')
            external_data.pop('main')
            external_data.pop('clouds')
            external_data.pop('weather')

            external_data['ip'] = ip
            external_data['ssid'] = secrets['SSID']
            external_data['boot time'] = time()
            sleep_ms(100)
            success = 1
            del ujson

        except ValueError as err:
            from quicktools import logger
            logger(f"{err} {time()}")
            del logger
            print(err)
            external_data.clear()
    sleep_ms(200)
    del get, secrets
    while True:
        try:
            external_data['games'] = get_free_games_names_from_epic()
            print("downloaded")
            break
        except ValueError as error:
            from quicktools import logger
            logger(f"{error} {time()}\n")
            del logger
            print(error)
    sleep_ms(100)
    return external_data

# def t_get_external_data():
#     ext_data = {'timezone': 3600, 'weather condition': 'clear sky', "clouds": 50, 'real temperature': 2,
#                 'real feel temperature': 1, 'pressure': 1000, 'humidity': 12, 'boot time': time(), 'sunrise': 123455,
#                 'sunset': 123456, 'country': 'country', 'city': 'city', 'ip': '123.234.244.244', 'ssid': 'ssid'}
#     sleep_ms(100)
#     return ext_data

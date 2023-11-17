from machine import ADC
from time import time, localtime
from random import randint

def logger(log, log_file: str = 'logs.txt'):
    with open(log_file, 'a') as log_writer:
        log_writer.write(log)


def del_logs(log_file: str = 'logs.txt'):
    with open(log_file, 'w') as log_cleaner:
        log_cleaner.write('LOGS : ')


def get_time(t: tuple = localtime(time())):
    return f"{t[3]}:{t[4]}:{t[5]}"


def get_date(t: tuple = localtime(time())):
    return f"{t[2]}/{t[1]}/{t[0]}"


def get_day(day_number: int = localtime(time())[6]):
    day_dict = {0: 'Monday',
                1: 'Tuesday',
                2: 'Wednesday',
                3: 'Thursday',
                4: 'Friday',
                5: 'Saturday',
                6: 'Sunday', }
    return day_dict[day_number]


# def brg_to_hex(*argv: int):
#     """converts brg values from 0 to 255 into hex (0-16)"""
#     converted_l = []
#     for arg in argv:
#         if arg > 255:
#             arg = 255
#         converted_l.append(str(hex(round((arg / 255) * 15)))[2])
#     return int(hex(int(''.join(converted_l), 16)))


def brg_to_hex(brg):
    """converts brg values from 0 to 255 into hex (0-16)"""
    return int('%02x%02x%02x' % brg, 16)


def get_int_temp(sensor: ADC):
    """reads the temperature on board"""
    conv_fact = 3.3 / 65535
    reading = sensor.read_u16() * conv_fact
    return round(27 - (reading - 0.706) / 0.001721)


def convert_epoch_to_normal(timestamp):
    return f"{localtime(timestamp)[3]}:{localtime(timestamp)[4]}"


def weather_condition_from_icon(icon: str):
    d = dict.fromkeys(['01d', '01n'], 'clear sky') | dict.fromkeys(['02d', '02n'], 'few clouds')\
        | dict.fromkeys(['03d', '03n'], 'scattered clouds') | dict.fromkeys(['04d', '04n'], 'broken clouds')\
        | dict.fromkeys(['50d', '50n'], 'mist') | dict.fromkeys(['11d', '11n'], 'thunderstorm')\
        | dict.fromkeys(['09d', '09n'], 'shower rain') | dict.fromkeys(['10d', '10n'], 'rain')\
        | dict.fromkeys(['13d', '13d'], 'snow')

    return d[icon]

def shuffle(list_to_be_shuffled):
    list_size = len(list_to_be_shuffled)
    already_shuffled = []
    shuffled_list = [0 for i in range(list_size)]
    for i in range(list_size):
        new_ind = randint(0, list_size - 1)
        while new_ind in already_shuffled:
            new_ind = randint(0, list_size - 1)
        shuffled_list[new_ind] = list_to_be_shuffled[i]
        already_shuffled.append(new_ind)
    return shuffled_list
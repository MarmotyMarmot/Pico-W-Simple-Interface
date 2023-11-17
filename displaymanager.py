from machine import ADC
from dispinch3 import LCD_1inch3
from time import time, localtime, sleep_ms
from quicktools import brg_to_hex, get_int_temp, get_date, convert_epoch_to_normal, get_time, logger


class display:
    def __init__(self, lcd: LCD_1inch3, temperature_sens: ADC, external_data: dict,
                 front_color: int = brg_to_hex((255, 255, 255)), back_color: int = brg_to_hex((0, 0, 0)),
                 header_color: int = brg_to_hex((255, 255, 255))):
        """allows for easy management of what is on display of our LCD and creating simple 'GUI'"""
        # targeted lcd
        self.__lcd = lcd

        # Basically just down the header
        self.__free_height = 10

        # Resolution of display
        self.__max_height = 240
        self.__max_width = 240

        # colors
        self.__back_color = back_color
        self.__front_color = front_color
        self.__header_color = header_color
        # screen number
        self.__screen_number = 1

        # What is under the header in the 1 screen
        self.__text = []

        # Data needed for setting up the header
        self.__temperature_sens = temperature_sens
        self.__time = 0

        #
        self.__external_data = external_data

    def __setup_header(self):
        """
            Basic difference between the header and lines under the header is that header will be constantly refreshed
            (use for things like time, temperature etc.)
        """

        # construct the header
        self.__lcd.fill_rect(0, 0, 240, 8, self.__back_color)
        self.__lcd.text(f"{str(get_int_temp(self.__temperature_sens))}*C", 208, 0, self.__header_color)
        self.__lcd.text(f"{get_time(localtime(time() + self.__external_data['timezone']))}", 0, 0,
                        self.__header_color)
        self.__lcd.text(f"{get_date()}", 96, 0, self.__header_color)
        self.__lcd.line(0, 8, 240, 8, self.__header_color)

    def __show_first_screen(self):
        self.display_large_image('logo', 128, 128, (4, 5), 32, 32, 56, 60)

    def __show_second_screen(self):
        from quicktools import weather_condition_from_icon
        weather_condition = weather_condition_from_icon(self.__external_data['weather icon'])
        del weather_condition_from_icon

        self.__lcd.text(f"{weather_condition}",
                        238 - len(weather_condition)*8, 55, self.__front_color)
        self.__lcd.text(f"Clouds:{self.__external_data['cloud coverage']}%", 0, 52, self.__front_color)
        self.__lcd.text(f"Pressure:{self.__external_data['pressure']}mbar", 0, 25, self.__front_color)
        self.__lcd.text(f"Humidity:{self.__external_data['humidity']}%", 0, 38, self.__front_color)
        self.__lcd.line(0, 77, 240, 77, self.__front_color)

        self.__lcd.text(f"Temp Out:{round(self.__external_data['real temperature'], 1)}*C", 0, 94, self.__front_color)
        self.__lcd.text(f"RealFeel:{round(self.__external_data['real feel temperature'], 1)}*C", 0, 121,
                        self.__front_color)
        self.__lcd.line(0, 146, 240, 146, self.__front_color)

        self.__lcd.text(
            f"Sunrise {convert_epoch_to_normal(self.__external_data['sunrise'] + self.__external_data['timezone'])}", 0,
            205,
            self.__front_color)
        self.__lcd.text(
            f"Sunset {convert_epoch_to_normal(self.__external_data['sunset'] + self.__external_data['timezone'])}", 136,
            205, self.__front_color)

        try:
            if weather_condition == 'clear sky' or weather_condition == 'few clouds':
                if time() > self.__external_data['sunset'] or time() < self.__external_data['sunrise']:
                    self.__lcd.display_image(f'./weather/night/{weather_condition.replace(" ", "")}_r.raw',
                                             32, 32, 208, 20)
                else:
                    self.__lcd.display_image(f'./weather/day/{weather_condition.replace(" ", "")}_r.raw',
                                             32, 32, 208, 20)
            else:
                self.__lcd.display_image(f'./weather/both/{weather_condition.replace(" ", "")}_r.raw', 32, 32, 208, 20)

            sleep_ms(100)
            self.__lcd.display_image('./weather/const/temp_r.raw', 32, 32, 208, 94)
            sleep_ms(10)
            self.__lcd.display_image('./weather/const/sunrise_r.raw', 32, 32, 36, 163)
            sleep_ms(10)
            self.__lcd.display_image('./weather/const/sunset_r.raw', 32, 32, 168, 163)

        except OSError as err:
            logger(f'{err} : No such files as : {weather_condition.replace(" ", "")}_r.raw\n')
            print(err)
            print(f'No such file as : {weather_condition.replace(" ", "")}_r.raw')

    def __show_third_screen(self):
        self.__lcd.text(f"Free Games on Epic :", 0, 19, self.__front_color)
        last_taken_height = 0
        for ind, game in enumerate(self.__external_data['games'].keys()):
            self.__lcd.text(game, 0, 34 + ind*15, self.__front_color)
            last_taken_height = 34 + ind*15
        self.__lcd.text("Games are available till 16:00", 0, last_taken_height + 15, self.__front_color)

    def __show_fourth_screen(self):
        self.__lcd.text(f"Location:{self.__external_data['location']}", 0, 10, self.__front_color)
        self.__lcd.text(f"Last Boot Time:{get_time(localtime(self.__external_data['boot time'] + self.__external_data['timezone']))}",
                        0, 19, self.__front_color)
        self.__lcd.text(f"SSID:{self.__external_data['ssid']}", 0, 37, self.__front_color)
        self.__lcd.text(f"IP:{self.__external_data['ip']}", 0, 46, self.__front_color)

    def change_screen(self, screen_number):
        self.__screen_number = screen_number

    def just_display(self, lines: list[str], bg_col, lines_col):
        """for display of simple screen with few lines and background, useful for errors at startup"""
        self.__lcd.fill(bg_col)
        for ind, line in enumerate(lines):
            self.__lcd.text(line, 0, ind * 8, lines_col)
        self.__lcd.show()

    def refresh(self):
        self.__setup_header()
        self.__lcd.show()

    def refresh_all(self):
        """refresh the whole screen"""
        self.__lcd.fill(self.__back_color)
        self.__setup_header()
        if self.__screen_number == 1:
            self.__show_first_screen()
        elif self.__screen_number == 2:
            self.__show_second_screen()
        elif self.__screen_number == 3:
            self.__show_third_screen()
        elif self.__screen_number == 4:
            self.__show_fourth_screen()
        self.__lcd.show()

    def add_line(self, line: str, color, line_number: int = -1):
        """adds the line to the display, if line_number is not entered it will add the line under the last one"""
        if self.__free_height <= self.__max_height and len(line) <= self.__max_width:
            if line_number == -1:
                self.__text.append((line, color))
            else:
                self.__text.insert(line_number - 1, (line, color))
            self.__free_height = self.__free_height + 9
        elif len(line) > self.__max_width:
            print("Line is too long!")
        else:
            self.__text.pop(0)
            if line_number == -1:
                self.__text.append((line, color))
            else:
                self.__text.insert(line_number - 1, (line, color))
            self.__free_height = self.__free_height + 9

    def remove_line(self, number: int):
        """removes the line at given index, first line is on number 1"""
        if number <= len(self.__text):
            self.__text.pop(number - 1)
        else:
            print("That is not correct line number")

    def display_large_image(self, image_name: str, picture_width: int, picture_height: int, coord_ind: tuple[int, int], x_size_of_chunk: int, y_size_of_chunk: int
                            , x_start: int, y_start: int):
        f"""It displays the image which would normally be too big for the ram to display, main assumptions are :\n
        - image is in .raw format\n
        - chunks are saved as image_name'x_coord''y_coord'_r.raw (x_coord and y_coord are just coordinates for this chunk in the bigger picture, not pixels, just numbers)\n
        - image is not larger than screen"""
        image_chunks = [f"{image_name}{x}{y}" for x in range(int(picture_width/x_size_of_chunk)) for y in range(int(picture_height/y_size_of_chunk))]
        from quicktools import shuffle
        image_chunks = shuffle(image_chunks)
        del shuffle

        for image_part in image_chunks:
            sleep_ms(1)
            x_coord = int(image_part[coord_ind[0]])
            y_coord = int(image_part[coord_ind[1]])
            self.__lcd.display_image(f"./{image_name}/{image_part}_r.raw", x_size_of_chunk, y_size_of_chunk,
                                     x_start + x_coord * x_size_of_chunk, y_start + y_coord * y_size_of_chunk)
            self.__lcd.show()

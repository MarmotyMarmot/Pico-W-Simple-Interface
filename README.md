# pico-simple-interface
Simple interface for Raspberry Pi Pico W

UI created for Waveshare 19650 1.3 Inch LCD display

![IMG_20231114_162720](https://github.com/AntekBrudka/pico-w-simple-interface/assets/45321229/91354493-cbd0-4da3-95bf-0d44b2ede1c3)
                 
## Aim of the project
The original purpose of this project was to "hang" pico with display on the wall, thus allowing users to check information fast and without unnecessary costs.

## Design
UI consists of four screens:

### Main screen : 

![IMG_20231114_162749](https://github.com/AntekBrudka/pico-w-simple-interface/assets/45321229/fe2d5865-f825-402d-93aa-eb5727576063)

### Weather screen :

![IMG_20231114_162845](https://github.com/AntekBrudka/pico-w-simple-interface/assets/45321229/15c2fcf2-9848-4c36-9f41-a6b67b40d374)

### Free games available on the Epic Games site:

![IMG_20231114_162540](https://github.com/AntekBrudka/pico-w-simple-interface/assets/45321229/55e97acd-560c-4685-b079-1d940e428c4d)

### Basic info:

![IMG_20231114_162933](https://github.com/AntekBrudka/pico-w-simple-interface/assets/45321229/536fd825-585c-4d73-a8b1-c5a68fde12eb)

## Usage
Buttons on the right side of the screen are used for navigation (A for main, B for weather, X for games, and Y for basic info). 
It is worth noting, that the value displayed in the upper right corner of each tab is a temperature from the onboard sensor, hence, it is not very accurate. 
Screensaver is set to turn the display off after 5 minutes of inactivity. In order to refresh external data, the programme will automatically reset the device after one hour. 

## Installation
Before moving files to pico three things should be passed into the secrets.py:
 - Network SSID
 - Network password
 - OpenWeather key (easily obtainable from their site)
   
In the next step, all files from this repository should be saved into Pico's memory.

## Disclaimer
Although it is possible to fill the whole screen with an image, it is not recommended because of memory restrictions.

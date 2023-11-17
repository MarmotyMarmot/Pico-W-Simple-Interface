# pico-simple-interface
Simple interface for Raspberry Pi Pico W

UI created for Waveshare 19650 1.3 Inch LCD display

![IMG_20231114_162720](https://github.com/AntekBrudka/pico-w-simple-interface/assets/45321229/119944e0-7c51-4380-908e-cd9fdb7bff1d)
                 
## Aim of the project
The original purpose of this project was to "hang" pico with display on the wall, thus allowing users to check information fast and without unnecessary costs.

## Design
UI consists of four screens:

### Main screen : 

![IMG_20231114_162749](https://github.com/AntekBrudka/pico-w-simple-interface/assets/45321229/bcd954d2-d2a6-404b-8cf8-19635ab5754c)

### Weather screen :

![IMG_20231114_162845](https://github.com/AntekBrudka/pico-w-simple-interface/assets/45321229/0b449cef-5a5e-4488-87b0-c7dadb86617f)

### Free games available on the Epic Games site:

![IMG_20231114_162540](https://github.com/AntekBrudka/pico-w-simple-interface/assets/45321229/a3efacdb-599b-4f33-88f9-f5f7fbbc0eda)

### Basic info:

![IMG_20231114_162933](https://github.com/AntekBrudka/pico-w-simple-interface/assets/45321229/96854458-8bc8-4932-8356-3ca8cb9edca7)

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

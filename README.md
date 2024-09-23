# SMSkyPi
This is the minimal source code base to run a Raspberry Pi based Allsky camera fully automatical over night within a WiFi network. My first developments started in 2021, this is the updated minimal version.

## Requirements
### Hardware
- Raspberry Pi 3/4
- Raspberry Pi HQ camera
- Fisheye lens for 360 degree vision

### Software
- Raspberry Pi OS, e.g. Bookworm (https://www.raspberrypi.com/software/operating-systems/)
- python3, pip3
```sudo apt-get install python3-pip```
- ffmpeg
```sudo apt-get install ffmpeg```
- suntime
```sudo pip3 install suntime --break-system-packages```

## Installation
Extract the content of this repository as it is to /home/pi/.
Run the setup.sh script.

## Camera Adjustment
On the Pi run
```rpicam-vid -t 0 -l -o tcp://0.0.0.0:3333```

On another PC run VLC and open a network stream:
```tcp/h264://<ip_address>:3333```

### Run SkyPi
If the crontab is configured properly the SkyPi software will be launched after reboot. The script skypi/check_night_or_day.py will configure the night run settings according to sunset and sunrise in skypi/skypi_config.py if an internet connection is available. The base file for the actual skypi settings is skypi_config_orig.py. If no internet connection is available the last stored settings will be used.
Nightshots will be taken during the darkest night (approx. sunset+1,5h / sunrise-1,5h) using rpicam-still (successor of raspistill). The images will be stored in /home/pi/timelapse_night_yyyy-mm-dd/.
At the end of the night the script skypi/finish_night.py will create a timelapse video, a startrail and keograms in /home/pi/yyyy-mm-dd.

## Notes on Dome Heating
Experience showed that temperatures below 10 degrees Celsius lead to dew on the dome. Several solutions exist to prevent this issue.

1) An AllSky-cam DIY heating solution is described here:
https://github.com/hdiessner/Allskycam-heating

It seems that wiringpi is outdated, but pigs (https://abyz.me.uk/rpi/pigpio/) works for me.
Installation
```
https://abyz.me.uk/rpi/pigpio/download.html
git clone https://github.com/joan2937/pigpio
wget https://github.com/joan2937/pigpio/archive/master.zip
unzip master.zip
cd pigpio-master
make
sudo make install
```

To switch the relais for the heater ON use
```
pigs modes <PIN_NR> w
pigs w <PIN_NR> 1
```
To switch the relais for the heater OFF use
```
pigs modes <PIN_NR> w
pigs w <PIN_NR> 0
```

3) if the camera mount contains holes to allow airflow between the Raspberry Pi underneath the dome a simple while-true-loop will increase the CPU workload and therefore its temperature:
```
#file heat_loop.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
while True:
  pass
```

To start the heat loop run
```
python3 /home/pi/heat_loop.py
```

To stop the heat loop run
```
sudo kill $(pgrep -f 'python3 /home/pi/heatLoop.py')
```
## Debugging
Debug output may be enabled per file.

## Extensibility
The straightforward implementation allows simple extensions. For example the results could be sent automatically to a (shared) network drive, a telegram bot, via email to someone, etc. .

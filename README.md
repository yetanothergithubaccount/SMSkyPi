# SkyPi
This is the minimal source code base to run a Raspberry Pi based Allsky camera over night within a WiFi network.

## Requirements
### Hardware
- Raspberry Pi 3/4
- Raspberry Pi HQ camera

### Software
- Raspberry Pi OS, e.g. Bookworm
- Python3, pip3
```sudo apt install python3-pip```
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
If the crontab is configured properly the SkyPi software will be launched after reboot. The script skypi/check_night_or_day.py will configure the night run settings according to sunset and sunrise in skypi/skypi_config.py. The base file for the actual skypi settings is skypi_config_orig.py.
Nightshots will be taken during the darkest night (sunset+1,5h / sunrise-1,5h). The images will be stored in /home/pi/timelapse_night_yyyy-mm-dd. At the end of the night the script skypi/finish_night.py will create a timelapse video, a startrail and keograms in /home/pi/yyyy-mm-dd.

## Debugging
Debug output may be enabled per file.


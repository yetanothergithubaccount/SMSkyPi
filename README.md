# SkyPi
This is the minimal source code base to run a Raspberry Pi based Allsky camera.

## Requirements
### Hardware
- Raspberry Pi 3/4
- Raspberry Pi HQ camera

### Software
- Raspberry Pi OS, e.g. Bookworm
- Python3
- ffmpeg
```sudo apt-get install ffmpeg```
- suntime
```sudo pip3 install suntime --break-system-packages```

## Installation
Run the setup.sh script.

## Camera Adjustment
On the Pi run
```rpicam-vid -t 0 -l -o tcp://0.0.0.0:3333```

On another PC run VLC and open a network stream:
```tcp/h264://$ip_address:3333```

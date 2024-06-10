#!/bin/bash
#
# Simple SkyPi software setup script
#

add2crontab() {
  echo "insert: $1"
  (crontab -l 2>/dev/null; echo "$1") | crontab -
}

echo "Install ffmpeg"
sudo apt-get install ffmpeg -f

echo "Update python installation..."
sudo pip3 install suntime --break-system-packages

echo "Install SkyPi service."
sudo cp skypi.service /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable skypi.service
sudo systemctl start skypi.service

#sudo systemctl status skypi.service

echo "SkyPi service is enabled and started."

echo "Update crontab"
crontab -r

add2crontab "@reboot sudo rm -f /home/pi/NIGHTSHOTS_RUNNING"
add2crontab "# check day/night time and launch automatic services accordingly"
add2crontab "@reboot sleep 90 && python3 /home/pi/check_night_or_day.py"

python3 skypi/check_night_or_day.py

echo "SkyPi installation succeeded."

read -n1 -p "Reboot SkyPi now? [y,n]" doit 
case $doit in
  y|Y) sudo reboot now ;;
  n|N) echo "SkyPi should be ready after a reboot." ;;
esac




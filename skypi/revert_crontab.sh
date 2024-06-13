#!/bin/bash
#
# Revert crontab, update SkyPi functionality
#
# Copyright (C) 2021++  Solveigh Matthies
#

# empty crontab
crontab -r
echo "crontab emptied"

add2crontab() {
  echo "insert: $1"
  (crontab -l 2>/dev/null; echo "$1") | crontab -
}

add2crontab "@reboot sleep 80 && /home/pi/skypi/revert_crontab.sh"
#add2crontab "@reboot sleep 120 && /home/pi/revert_crontab.sh" # do it again just in case the wifi took longer to connect to

add2crontab "# check day/night time and launch automatic services accordingly"
add2crontab "@reboot sleep 90 && python3 /home/pi/skypi/check_night_or_day.py"
add2crontab "@reboot sleep 75 && /home/pi/skypi/is_nightshots_running.sh"

add2crontab "@reboot sudo rm -f /home/pi/NIGHTSHOTS_RUNNING"

echo "crontab reverted to original content"

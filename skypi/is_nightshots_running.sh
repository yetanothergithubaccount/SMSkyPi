#!/bin/bash
#
# Detect whether SkyPi nightshots are running
#
# Copyright (C) 2021++  Solveigh Matthies
#

pid=$(pgrep -f '/usr/bin/bash /home/pi/skypi/nightshotservice.sh')

echo "PID: " $pid

if [ -z "$pid" ]
then
  echo "SkyPi: system launched nightshots are NOT running"
else
  echo "SkyPi: system launched nightshots are running"
fi

exit 0

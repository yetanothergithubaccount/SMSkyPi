#!/bin/bash
#
# Detect whether SkyPi nightshots are running
#
# Copyright (C) 2021++  Solveigh Matthies
#
# This program is free software: you can redistribute it and/or modify it 
# under the terms of the GNU General Public License as published by the 
# Free Software Foundation, either version 3 of the License, or a later version.
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

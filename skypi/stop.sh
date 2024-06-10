#!/bin/bash
#
# Stop SkyPi night mode
#
# Copyright (C) 2021++  Solveigh Matthies
#
# This program is free software: you can redistribute it and/or modify it 
# under the terms of the GNU General Public License as published by the 
# Free Software Foundation, either version 3 of the License, or a later version.
#

sudo systemctl stop skypi.service
sudo rm /home/pi/NIGHTSHOTS_RUNNING
echo "SkyPi night mode stopped."

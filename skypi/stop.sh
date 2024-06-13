#!/bin/bash
#
# Stop SkyPi night mode
#
# Copyright (C) 2021++  Solveigh Matthies
#

sudo systemctl stop skypi.service
sudo rm /home/pi/NIGHTSHOTS_RUNNING
echo "SkyPi night mode stopped."

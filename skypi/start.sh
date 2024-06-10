#!/bin/bash
#
# Create directory for the nights pictures
# Launch SkyPi night mode
#
# Copyright (C) 2021++  Solveigh Matthies
#
# This program is free software: you can redistribute it and/or modify it 
# under the terms of the GNU General Public License as published by the 
# Free Software Foundation, either version 3 of the License, or a later version.
#

if [ ! -d $imagesDIR ]
then
  echo "$imagesDIR does not exist yet."
  # create images directory
  date=$(date '+%d.%m.%Y')
  imagesDIR="/home/pi/timelapse_night_$date"
  mkdir $imagesDIR
  sleep 2
fi

if [ -d $imagesDIR ] 
then
	#sudo service skypi start
	sudo systemctl start skypi.service
	echo "SkyPi night mode started"
else
	echo "SkyPi night mode: $imagesDIR does not exist"
fi

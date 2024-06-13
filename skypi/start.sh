#!/bin/bash
#
# Create directory for the nights pictures
# Launch SkyPi night mode
#
# Copyright (C) 2021++  Solveigh Matthies
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

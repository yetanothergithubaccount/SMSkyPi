#!/bin/bash
#
# Insert into crontab: launch timelapse video, startrail and keogram 
#  etc creation script at a given time via crontab.
# Optional: shutdown at the end
#
# Copyright (C) 2021++  Solveigh Matthies
#
# This program is free software: you can redistribute it and/or modify it 
# under the terms of the GNU General Public License as published by the 
# Free Software Foundation, either version 3 of the License, or a later version.
#

echo "Start time: $1:$2"

crontab -l > crontab.txt

res=$(grep -i "finish_night.py" "/home/pi/crontab.txt")
if [ -z "$res" ]
then
  #(crontab -l 2>/dev/null; echo "$2 $1 * * * python3 /home/pi/skypi/finish_night.py") | crontab -
  (crontab -l 2>/dev/null; echo "$2 $1 * * * python3 /home/pi/skypi/finish_night.py --shutdown") | crontab -
	echo "Launch night startrail and time-lapse video creation at $1:$2"

else
	echo "Night startrail and time-lapse video creation at $1:$2 NOT added again to crontab"
fi



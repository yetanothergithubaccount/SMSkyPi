#!/bin/bash
# -*- coding: utf-8 -*-
#
# start script to take night shots, run by nightshots.service
#
# Copyright (C) 2021++  Solveigh Matthies
#

while true
do
  # run nightshot script regularly
  python3 /home/pi/skypi/nightshots.py
  #sleep 1 #10	# seconds # 0.5
done

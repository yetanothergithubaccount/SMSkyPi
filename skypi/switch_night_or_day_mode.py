#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Switch to day or night mode, start/stop SkyPi service accordingly
#
# Copyright (C) 2021++  Solveigh Matthies
#

import os
import time, datetime
from datetime import datetime
from datetime import date
import shutil

import skypi_config

debug = False #True #False

NIGHT_START_H = skypi_config.nightshots['NIGHT_START_H'] #20
NIGHT_END_H = skypi_config.nightshots['NIGHT_END_H'] #6

NIGHT_START_M = skypi_config.nightshots['NIGHT_START_M'] #5
NIGHT_END_M = skypi_config.nightshots['NIGHT_END_M'] #15

SUMMER = skypi_config.nightshots['SUMMER'] #"summer"
WINTER = skypi_config.nightshots['WINTER'] #"winter"

theSeason = SUMMER

if __name__ == '__main__':
  try:
    now = datetime.now()
    theDate = str(now.strftime("%Y-%m-%d"))
    #print(now.strftime("%Y-%m-%d %H:%M"))
    theMonth = int(now.strftime("%m"))
    theTime = now.strftime("%H:%M")
    theHour = int(now.strftime("%H"))
    theMinute = now.strftime("%M")

    msg = now.strftime("%Y-%m-%d %H:%M") + ": \n"
    if debug:
      print("Now: " + str(msg))
    print("SkyPi: Adapt day/night mode: " + str(msg))

    # print("The month: " + str(theMonth))
    if 5 <= theMonth and theMonth <= 9:
      if debug:
        print("Summer time: " + str(theTime))
      theSeason = SUMMER
      if theHour >= (int(NIGHT_START_H)-1) or theHour < NIGHT_END_H:
        if debug:
          print("Night time (" + str(theSeason) + ")")
          print("SkyPi: check day/night: night (summer)")

        print("SkyPi: Start nightshots service")
        os.system("/home/pi/skypi/start.sh")

        exit(1)
      else:
        if debug:
          print("Day time (" + str(theSeason) + ")")
          print("SkyPi: check day/night: night (summer)")

        print("SkyPi: Stop nightshots service")
        os.system("/home/pi/skypi/stop.sh")

        exit(0)
    else:
      if debug:
          print("Winter time: " + str(theTime))
      theSeason = WINTER
      if theHour >= (int(NIGHT_START_H)-1) or theHour < NIGHT_END_H:
        if debug:
          print("Night time (" + str(theSeason) + ")")
          print("SkyPi: check day/night: night (winter)")

        print("SkyPi: Start nightshots service")
        os.system("/home/pi/skypi/start.sh")

        exit(1)
      else:
        if debug:
          print("Day time (" + str(theSeason) + ")")
          print("SkyPi: check day/night: day (winter)")

        print("SkyPi: Stop nightshots service")
        os.system("/home/pi/skypi/stop.sh")

        exit(0)

  except Exception as e:
    print("SkyPi: switch mode error: " + str(e))

  exit(0)

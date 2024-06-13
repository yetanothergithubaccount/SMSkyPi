#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# check sunrise/sunset times for the location to determine
#   the settings for the nightshots and the result creation
#   at the end of the amateurastronomical night
#
# Copyright (C) 2021++  Solveigh Matthies
#

import os
import time, datetime
from datetime import datetime
from datetime import date
from datetime import timedelta
import shutil
import pytz
from suntime import Sun, SunTimeException

debug = False #True #False

import skypi_config
latitude, longitude = skypi_config.coordinates["latitude"], skypi_config.coordinates["longitude"] #'49.878708','8.646927'
location = skypi_config.coordinates["location"]

sun = Sun(latitude, longitude)

if __name__ == '__main__':
  try:
    now = datetime.now()
    theDate = str(now.strftime("%Y-%m-%d"))
    #print(now.strftime("%Y-%m-%d %H:%M"))
    theMonth = int(now.strftime("%m"))
    theTime = now.strftime("%H:%M")
    theHour = int(now.strftime("%H"))
    theMinute = now.strftime("%M")

    if debug:
      print("SkyPi: check mode at " + str(now.strftime("%Y-%m-%d %H:%M")))

    # On a special date in your machine's local time zone
    dd = theDate.split('-')
    if len(dd) == 3:
      for_date = date(int(dd[0]), int(dd[1]), int(dd[2]))
      abd = for_date
      sun = Sun(latitude, longitude)
      tz = pytz.timezone(skypi_config.nightshots["timezone"])
      today_sr = sun.get_sunrise_time()
      today_ss = sun.get_sunset_time()
      if debug:
        print(today_sr.astimezone(tz))
        print(today_ss.astimezone(tz))
      today_sr = today_sr.astimezone(tz)
      today_ss = today_ss.astimezone(tz)

      if today_sr != None and today_ss != None:
        if debug:
          print("On " + str(abd.strftime('%Y-%m-%d')) + " at " + str(location) + " the sun raises at " + str(today_sr.strftime('%H:%M')) + " and will set at " + str(today_ss.strftime('%H:%M')) + " UTC")
        msg = "*" + str(theDate) + ":*\n"
        msg += "Sunrise: " + str(today_sr.strftime('%H:%M')) + "\n"
        msg += "Sunset: " + str(today_ss.strftime('%H:%M'))

        # suggest start/end times according to sunrise/sunset
        # e.g. sunrise - 1.20, sunset + 1.20

        today = date.today()
        yesterday = today - timedelta(days=1)
        tomorrow = today + timedelta(days=1)
        if debug:
          print("Now: " + str(now))
          print("Today: " + str(today))
          print("Tomorrow: " + str(tomorrow))

        # NIGHT mode:
        todayNightStart = now.replace(hour=int(str(today_ss.strftime('%H:%M')).split(":")[0]), minute=int(str(today_ss.strftime('%H:%M')).split(":")[1]), second=0, microsecond=0)
        tomorrowNightEnd = now.replace(day=int(tomorrow.strftime("%d")),month=int(tomorrow.strftime("%m")),year=int(tomorrow.strftime("%Y")), hour=int(str(today_sr.strftime('%H:%M')).split(":")[0]), minute=int(str(today_sr.strftime('%H:%M')).split(":")[1]), second=0, microsecond=0)
        todayNightStart = todayNightStart + timedelta(hours=1, minutes=31)
        tomorrowNightEnd = tomorrowNightEnd - timedelta(hours=1, minutes=31)
        
        tomorrowNightEnd_hour = int(str(tomorrowNightEnd.strftime("%H")))
        tomorrowNightEnd_minute = int(str(tomorrowNightEnd.strftime("%M")))
        if tomorrowNightEnd_minute == 60:
          tomorrowNightEnd_hour = tomorrowNightEnd_hour+1
          tomorrowNightEnd_minute = 0
          if debug:
            print("End min night == 60")
        tomorrowNightEnd = now.replace(day=int(tomorrow.strftime("%d")),month=int(tomorrow.strftime("%m")),year=int(tomorrow.strftime("%Y")), hour=int(tomorrowNightEnd_hour), minute=int(tomorrowNightEnd_minute), second=0, microsecond=0)
        if debug:
          print("Start time night: " + str(todayNightStart))
          print("End time night: " + str(tomorrowNightEnd))

        if not os.path.exists("/home/pi/timelapse_night_" + str(theDate)):
          os.makedirs("/home/pi/timelapse_night_" + str(theDate))
          if debug:
            msg = "Directory /home/pi/timelapse_night_" + str(theDate) + " created."
            print(msg)

        # rewrite /home/pi/skypi/skypi_config.py
        try:
          # create a backup of the latest configuration
          if not os.path.exists('/home/pi/skypi/backup_config/'):
            os.makedirs('/home/pi/skypi/backup_config/')
          shutil.copy2('/home/pi/skypi/skypi_config.py', '/home/pi/skypi/backup_config/skypi_config_' + str(theDate) + '.py') # preserve timestamp

          file = open('/home/pi/skypi/skypi_config_orig.py', 'r')
          lines = file.readlines()

          # replace start/end times in skypi_config.py
          file1 = open('/home/pi/skypi/skypi_config.py', 'w')
          for line in lines:
            if 'NIGHT_START_H' in line:
              file1.write('  NIGHT_START_H = ' + str(int(todayNightStart.strftime("%H"))) + ' ,\n')
            elif 'NIGHT_START_M' in line:
              file1.write('  NIGHT_START_M = ' + str(int(todayNightStart.strftime("%M"))) + ' ,\n')
            elif 'NIGHT_END_H' in line:
              file1.write('  NIGHT_END_H = ' + str(int(tomorrowNightEnd.strftime("%H"))) + ' ,\n')
            elif 'NIGHT_END_M' in line:
              file1.write('  NIGHT_END_M = ' + str(int(tomorrowNightEnd.strftime("%M"))) + ' ,\n')
            else:
              file1.write(line)
          file1.close()

          time.sleep(2)

          print("Night: Run from " + str(todayNightStart.strftime("%H")) + ":" + str(todayNightStart.strftime("%M")) + " to " + str(tomorrowNightEnd.strftime("%H")) + ":" + str(tomorrowNightEnd.strftime("%M")))

          # create a non-permanent cronjob for the video etc creation
          endNight = tomorrowNightEnd + timedelta(hours=0, minutes=1)
          endHourNight = endNight.strftime('%H')
          endMinNight = endNight.strftime('%M')

          if debug:
            print("End of night, start cronjob: " + str(endHourNight) + ":" + str(endMinNight))
          os.system("/home/pi/skypi/cronjob_finish_night.sh " + str(endHourNight) + " " + str(endMinNight))

        except Exception as e:
          print("SkyPi ERROR: " + str(e))

        msg = now.strftime("%Y-%m-%d %H:%M") + ": \n"
        if debug:
          print("Now: " + str(msg))
      else:
        endHourNight = skypi_config.nightshots["NIGHT_END_H"]
        endMinNight = skypi_config.nightshots["NIGHT_END_M"]
        os.system("/home/pi/skypi/cronjob_finish_night.sh " + str(endHourNight) + " " + str(endMinNight))
        msg = "SkyPi: check mode error: could not update sunrise/sunset times. End at " + str(endHourNight) + ":" + str(endMinNight)
        if debug:
          print(msg)

      os.system("python3 /home/pi/skypi/switch_night_or_day_mode.py")

  except Exception as e:
    print("SkyPi check mode error: " + str(e))
    exit(0)

  exit(0)

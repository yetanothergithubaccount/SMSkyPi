#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# script to take night shots, run by nightshots.service
#
# Copyright (C) 2021++  Solveigh Matthies
#

import time, datetime
from time import sleep
from datetime import datetime
from datetime import date
from datetime import timedelta
import json
import requests
import socket
import sys, os
import os.path
from os import path
from os.path import dirname

sys.path.append(dirname("/home/pi/"))
import skypi_config

debug = False #True #False

imagesDIR_base = "/home/pi/timelapse_"

filename = skypi_config.nightshots['filename']  #"/home/pi/NIGHTSHOTS_RUNNING"
imagesDIR_night = "night_"

_START_H = skypi_config.nightshots['NIGHT_START_H']
_START_M = skypi_config.nightshots['NIGHT_START_M']
_END_H = skypi_config.nightshots['NIGHT_END_H']
_END_M = skypi_config.nightshots['NIGHT_END_M']

'''
if debug:
  now = datetime.now()
  _START_H = int(now.strftime("%H"))
  _START_M = int(now.strftime("%M"))
  if int(now.strftime("%H"))+1<23:
    _END_H = int(now.strftime("%H"))+1
  else:
    _END_H = 0
  if int(now.strftime("%M"))+1<59:
    _END_M = int(now.strftime("%M"))+1
  else:
    _END_M = 0
'''
width = skypi_config.nightshots['width'] #1920 3200
height = skypi_config.nightshots['height'] #1440 2400

ISO = skypi_config.nightshots['ISO'] #800
timespan = skypi_config.nightshots['timespan'] #6000000  # 1 minute
brightness = skypi_config.nightshots['brightness'] #80
contrast = skypi_config.nightshots['contrast'] #100
awbgain_blue = skypi_config.nightshots['awbgain_blue']
awbgain_red = skypi_config.nightshots['awbgain_red']
quality = skypi_config.nightshots['quality'] #90 # 100
sharpness = skypi_config.nightshots['sharpness'] #1.5
awb_mode = skypi_config.nightshots['awb_mode']
exp_mode = skypi_config.nightshots['exp_mode']

STARTED="started"
FINISHED="finished"

image_name_format = "%Y-%m-%d__%H.%M.%S"
date_format = "%Y-%m-%d"
time_format = "%H:%M"

#########################FILE#############################
def readFile(fileName):
  state=""
  try:
    target = open(fileName, 'r')
    state = target.read()
    target.close()
    #print('Read shot state in ' + fileName + ': ' + str(state))
  except Exception:
    pass
  return state

def writeFile(fileName, state):
  try:
    #print('Store shot state in ' + fileName + ': ' + str(state))
    target = open(fileName, 'w')
    target.write(str(state))
    target.close()
    if debug:
      print("*SHOTS_RUNNING file written: " + str(datetime.now().strftime(image_name_format)))
  except Exception:
    return False
  return True

def fileExists(fileName):
  if debug:
    print("Check *SHOTS_RUNNING file exists: " + str(datetime.now().strftime(image_name_format)))
  if os.path.exists(fileName):
    if debug:
      print("*SHOTS_RUNNING file exists: " + str(datetime.now().strftime(image_name_format)))
    return True
  if debug:
    print("*SHOTS_RUNNING file does not exist: " + str(datetime.now().strftime(image_name_format)))
  return False

def removeFile(fileName):
  try:
    if fileExists(fileName):
      if debug:
        print("Remove file: " + str(fileName))
      os.remove(fileName)
      if debug:
        print("File " + str(fileName) + " removed.")
  except Exception as e:
    pass
######################END##FILE###########################

if __name__ == '__main__':
  try:
    now = datetime.now()
    theHour = now.strftime("%H")

    msg = now.strftime(str(date_format) + " " + str(time_format)) + ": \n"

    if debug:
      print("Now: " + str(now.strftime("%Y-%m-%d %H:%M")))
      print("START: " + str(_START_H) + ":" + str(_START_M))
      print("END: " + str(_END_H) + ":" + str(_END_M))

    today = date.today()
    yesterday = today - timedelta(days=1)
    tomorrow = today + timedelta(days=1)
    if debug:
      print("Now: " + str(now))
      print("The hour: " + str(theHour))
      print("Yesterday: " + str(yesterday.strftime("%Y-%m-%d")))
      print("Today: " + str(today.strftime("%Y-%m-%d")))
      print("Tomorrow: " + str(tomorrow.strftime("%Y-%m-%d")))
      print("File " + str(filename) + " exists: " + str(fileExists(filename)))

    todayStart = now.replace(hour=_START_H, minute=_START_M, second=0, microsecond=0)
    yesterdayStart = todayStart
    tomorrowEnd = now.replace(day=int(tomorrow.strftime("%d")),month=int(tomorrow.strftime("%m")),year=int(tomorrow.strftime("%Y")), hour=_END_H, minute=_END_M, second=0, microsecond=0)
    if debug:
      print("Now: " + str(now))
      print("Yesterday start: " + str(yesterdayStart.strftime("%Y-%m-%d %H:%M")))
      print("Today start: " + str(todayStart.strftime("%Y-%m-%d %H:%M")))
      print("Tomorrow end: " + str(tomorrowEnd.strftime("%Y-%m-%d %H:%M")))
    
    if ((int(theHour) >= 0) and (int(theHour) <= int(_END_H))):
      # after midnight, nightshots still running since last night
      tomorrow = today

      # after midnight
      #if ((int(theHour) >= 0) and (int(theHour) <= int(_END_H))): # and fileExists(filename): # save a disk operation
      yesterdayStart = now.replace(day=int(yesterday.strftime("%d")),month=int(yesterday.strftime("%m")),year=int(yesterday.strftime("%Y")), hour=_END_H, minute=_END_M, second=0, microsecond=0)

    if ((now >= todayStart) or (now > yesterdayStart)) and (now <= tomorrowEnd):
      if debug:
        print("Within nightshots time.")

      if fileExists(filename) == False:
        writeFile(filename, 1)

      addendum = now.strftime(str(image_name_format))
      addendumDIR = now.strftime(str(date_format))
            
      #if (now > yesterdayStart) and (now <= tomorrowEnd):  # after midnight
      if ((int(theHour) >= 0) and (int(theHour) <= int(_END_H))):
        if debug:
          print("After midnight: " + str(yesterdayStart.strftime(str(date_format))))
        addendumDIR = yesterdayStart.strftime(str(date_format))

      imagesDIR = str(imagesDIR_base) + str(imagesDIR_night) + str(addendumDIR)

      if debug:
        print("Images directory: " + str(imagesDIR))

      image = str(imagesDIR) + "/image_" + str(addendum) + ".jpg"

      if ((int(theHour) >= 0) and (int(theHour) <= int(_END_H))):          # after midnight
        addendum_yesterday = yesterday.strftime(str(image_name_format))  # use the images directory from yesterday
        addendum_yesterdayDIR = yesterday.strftime(str(date_format))

        image = str(imagesDIR_base) + str(imagesDIR_night) + str(addendum_yesterdayDIR) + "/image_" + str(addendum) + ".jpg"
        if debug:
          print("After midnight: use directory from yesterday: " + str(image))

        # NIGHT SHOT
        # last known working raspistill command (2021)
        #cmd = "raspistill -w " + str(width) + " -h " + str(height) + " -ISO " + str(ISO) + " --awb " + str(awb_mode) + " --shutter " + str(timespan) + " --drc low --nopreview --metering average --thumb none --quality 100 --exposure " + str(exp_mode) + " --flicker off --analoggain 8 --mode 3 --timeout 3000 --digitalgain 1 --stats --burst -o " + str(image)
                
      # 2024: new rpicam-still command
      cmd="rpicam-still --width " + str(width) + " --height " + str(height) + " --shutter " + str(timespan) + " --gain " + str(int(ISO/100)) + " --immediate --nopreview --denoise off --sharpness " + str(sharpness) + " -q " + str(quality) + " --awbgains " + str(awbgain_red) + "," + str(awbgain_blue) + " -o " + str(image) #2.5,2.5
      # --lens-position 0.0 : takes too much time

      if debug:
        print(cmd)
      ret = os.system(cmd)

      if debug:
        print("Nightshot command: " + str(cmd))
        print("Nightshot returned: " + str(ret))

  except Exception as e:
    msg = "SkyPi nightshots error: "
    print(str(msg) + str(e))
    removeFile(filename)
    exit(0)

  exit(0)


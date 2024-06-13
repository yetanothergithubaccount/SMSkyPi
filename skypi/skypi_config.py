#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SkyPi configuration
#
# Copyright (C) 2021++  Solveigh Matthies
#

coordinates = dict(
  latitude = 49.87533,
  longitude = 8.65345,
  location = 'Darmstadt'
)

nightshots = dict(
  #width = 4056,
  #height = 3040,
  #width = 3200,
  #height = 2400,

  width=1920,
  height=1440,

  ISO = 800,

  #timespan = 60000000, # 1 minute
  timespan = 20000000, # 20 seconds

  brightness = 80,
  contrast = 100,
  
  awbgain_red = 2.3,
  awbgain_blue = 2.3,

  quality = 100,     # JPEG quality
  sharpness = 1.5,

  awb_mode = "off", # auto, incandescent, tungsten, fluorescent, indoor, daylight, cloudy, custom
  exp_mode = "off", # off, auto, night, nightpreview, backlight, spotlight, sports, snow, beach, verylong, fixedfps, antishake, fireworks

  SUMMER = "summer",
  WINTER = "winter",

  NIGHT_START_H = 9 ,
  NIGHT_START_M = 51 ,

  NIGHT_END_H = 4 ,
  NIGHT_END_M = 51 ,

  filename = "/home/pi/NIGHTSHOTS_RUNNING",
  timezone = 'Europe/Berlin'
)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Create a startrail from last nights SkyPi images. Inspired by
#   http://www.tobias-westmeier.de/astronomy_tutorial_startrails.php
#
# Optional: filter images according to airplane night breaks.
#
# Copyright (C) 2021++  Solveigh Matthies
#
# This program is free software: you can redistribute it and/or modify it 
# under the terms of the GNU General Public License as published by the 
# Free Software Foundation, either version 3 of the License, or a later version.
#

import os, sys, platform
import numpy
from PIL import Image
import time, datetime
from datetime import datetime
from datetime import date
from datetime import timedelta

import optparse
parser = optparse.OptionParser()

debug = False #True #False

theDate = time.strftime("%Y-%m-%d")
theDateAndTime = time.strftime("%Y-%m-%d_%H-%M-%S")
today = date.today()
yesterday = today - timedelta(days=1)
date_yesterday = yesterday.strftime("%Y-%m-%d")

parser.add_option('-d', '--date',
    action="store", dest="date",
    help="Date", default=str(date_yesterday))
parser.add_option('-a', '--aftereleven',
    action="store", dest="aftereleven",
    help="After eleven o'clock", default=False)
parser.add_option('-b', '--afterelevenbeforefive',
    action="store", dest="afterelevenbeforefive",
    help="After eleven o'clock, before five o'clock to minimise airplane sightings", default=False)
parser.add_option('-f', '--folder',
    action="store", dest="folder",
    help="Image folder")

options, args = parser.parse_args()

theDate = options.date
after_eleven = options.aftereleven
after_eleven_before_five = options.afterelevenbeforefive
image_dir = "/home/pi/timelapse_night_" + str(theDate)
results_dir = "/home/pi/" + str(theDate)

if options.folder:
  image_dir = options.folder

if debug:
  print("Work with images in directory " + str(image_dir))

#########################MAIN#############################
if __name__ == "__main__":

  try:
    files = os.listdir(image_dir)
    #images = [name for name in files if name[-4:] in [".jpg", ".JPG"]]
    if after_eleven:
      images = [name for name in files if (name[-4:] in [".jpg", ".JPG"]) and (name[0] == "i") and (name[0] != "S") and (name[0] != "K") and (not "__17." in name) and (not "__18." in name) and (not "__19." in name) and (not "__20." in name) and (not "__21." in name) and (not "__22." in name)]
    elif after_eleven_before_five:
      images = [name for name in files if (name[-4:] in [".jpg", ".JPG"]) and (name[0] == "i") and (name[0] != "S") and (name[0] != "K") and (not "__17." in name) and (not "__18." in name) and (not "__19." in name) and (not "__20." in name) and (not "__21." in name) and (not "__22." in name) and (not "__05." in name) and (not "__06." in name) and (not "__07." in name)]
    else:
      images = [name for name in files if (name[-4:] in [".jpg", ".JPG"]) and (name[0] == "i") and (name[0] != "S") and (name[0] != "K")]
    #if debug:
    #  for img in images:
    #    print(img)

    start_time = time.time()
    
    width, height = Image.open(str(image_dir) + "/" + str(images[0])).size
    stack   = numpy.zeros((height, width, 3), float)
    counter = 1
    current_image = ""

    images = sorted(images)

    for image in images:
      #print("Processing image " + str(counter))
      current_image = str(image_dir) + "/" + str(image)
      image_new = numpy.array(Image.open(current_image), dtype = float)

      image_new_dim = image_new.shape
      stack_dim = stack.shape
      if debug:
        print("Image new dimensions: " + str(image_new_dim))
        print("Stack dimensions: " + str(stack_dim))
      if image_new_dim == stack_dim:
        stack = numpy.max([stack, image_new], axis=0) # slower
        counter  += 1
        if debug:
          print("Startrail: stacking " + str(current_image) + " [" + str(counter) + "]")

    stack = numpy.array(numpy.round(stack), dtype = numpy.uint8)

    output = Image.fromarray(stack, mode = "RGB")
    if after_eleven:
      out_image = str(results_dir) + "/" + "StarTrail_" + str(date_yesterday) + "_23pp.jpg"
    elif after_eleven_before_five:
      out_image = str(results_dir) + "/" + "StarTrail_" + str(date_yesterday) + "_23pp5.jpg"
    else:
      out_image = str(results_dir) + "/" + "StarTrail_" + str(date_yesterday) + ".jpg"
    output.save(str(out_image), "JPEG", compress_level=1, quality=100)

    end_time = time.time()
    elapsed_time = end_time - start_time

    if debug:
      print("Elapsed time: " + str(elapsed_time) + " s")
      msg = "SkyPi: Startrail image saved: " + str(out_image) + " (" + str(round(elapsed_time,2)) + " s)"
      print(msg)
  except Exception as e:
    msg = "Skypi startrail error: " + str(e)
    print(msg)
  sys.exit(0)

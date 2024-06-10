#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Create vertical or horizontal keogram from last nights SkyPi images
#
# Copyright (C) 2021++  Solveigh Matthies
#
# This program is free software: you can redistribute it and/or modify it 
# under the terms of the GNU General Public License as published by the 
# Free Software Foundation, either version 3 of the License, or a later version.
#

import os, sys
import numpy
from PIL import Image
import time, datetime
from datetime import datetime
from datetime import date
from datetime import timedelta
import time

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
parser.add_option('-v', '--vertical',
    action="store_true", dest="vertical",
    help="vertical slices")
parser.add_option('-o', '--horizontal',
    action="store_true", dest="horizontal",
    help="horizontal slices")
options, args = parser.parse_args()

theDate = options.date
image_dir = "/home/pi/timelapse_night_" + str(theDate)
results_dir = "/home/pi/" + str(theDate)

if __name__ == '__main__':
  try:
    files   = os.listdir(image_dir)
    files.sort()
    images  = [name for name in files if (name[-4:] in [".jpg", ".JPG"]) and (name[0] == "i")]

    start_time = time.time()

    width, height = Image.open(str(image_dir) + "/" + str(images[0])).size
    MODE =  "RGB"

    if debug:
      print("Image width: " + str(width) + ", height: " + str(height))
    w2 = int(width/2)
    h2 = int(height/2)
    if debug:
      print("w2: " + str(w2) + ", h2: " + str(h2))

    image_count = len(files)
    if debug:
      print("# images: " + str(image_count))

    if options.vertical:
      imageKeo = numpy.array(Image.new(MODE, (image_count, height)))
      if debug:
        print("Keogram dimensions: " + str(image_count) + "x" + str(height))
    elif options.horizontal:
      imageKeo = numpy.array(Image.new(MODE, (width, image_count)))
      if debug:
        print("Keogram dimensions: " + str(width) + "x" + str(image_count))
    counter = 0

    current_image = ""
    for image in images:
      if debug:
        print ("Processing image " + str(counter) + ", " + str(image))
      current_image = str(image_dir) + "/" + str(image)
      imageKeogram = numpy.array(Image.open(str(current_image)).convert(MODE))
      if options.vertical:
        imageKeo[:, counter] = numpy.copy(imageKeogram[:, w2])  # w2: take the center column
      elif options.horizontal:
        imageKeo[counter, :] = numpy.copy(imageKeogram[h2, :])  # h2: take the center row
      counter  += 1

    output = Image.fromarray(imageKeo, mode = MODE)
    mode = ""
    if options.vertical:
      out_image = str(results_dir) + "/" + "Keogram_" + str(date_yesterday) + "_v.jpg"
      mode = "vertical"
    elif options.horizontal:
      out_image = str(results_dir) + "/" + "Keogram_" + str(date_yesterday) + "_h.jpg"
      mode = "horizontal"
    output.save(str(out_image), "JPEG", compress_level=1, quality=100)

    end_time = time.time()
    elapsed_time = end_time - start_time
    if debug:
      print("Elapsed time: " + str(elapsed_time) + " s")

    msg = "SkyPi: " + str(mode) + " Keogram saved: " + str(out_image) + " (" + str(round(elapsed_time,2)) + " s)"
    if debug:
      print(msg)
  except Exception as e:
    msg = "Skypi keogram error: " + str(e)
    print(msg)

  sys.exit()

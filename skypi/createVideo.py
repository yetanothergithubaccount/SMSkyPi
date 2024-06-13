#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Timelapse video creation with ffmpeg
#
# sudo apt-get install -y ffmpeg
#
# Copyright (C) 2021++  Solveigh Matthies
#

import os, sys, os.path
from pathlib import Path
import time, datetime
from datetime import datetime
from datetime import date
from datetime import timedelta
import optparse
parser = optparse.OptionParser()

debug = False #True #False

parser.add_option('-d', '--date',
    action="store", dest="date",
    help="Date", default=str((date.today() - timedelta(days=1)).strftime("%Y-%m-%d")))
parser.add_option('-f', '--folder',
    action="store", dest="folder",
    help="Image folder")
parser.add_option('-n', '--name',
    action="store", dest="name",
    help="Video filename")
parser.add_option('-s', '--scale_down',
    action="store_true", dest="scale_down",
    help="Scale video to 640x480")

options, args = parser.parse_args()


#########################MAIN#############################
if __name__ == "__main__":
  try:
    theDate = time.strftime("%Y-%m-%d")
    theDateAndTime = time.strftime("%Y-%m-%d_%H-%M-%S")
    today = date.today()
    yesterday = today - timedelta(days=1)
    date_yesterday = yesterday.strftime("%Y-%m-%d")

    if options.date:
      theDate=options.date
    if debug:
      print("The date: " + str(theDate))

    imagesDIR="/home/pi/timelapse_night_" + str(theDate)
    fileName = "timelapse_night_" + str(theDate) + ".mp4"
    results_dir = "/home/pi/" + str(theDate)

    if options.folder:
      imagesDIR = options.folder
    if debug:
      print("Images directory: " + str(imagesDIR))

    if options.name:
      fileName=options.name
      #if options.scale_down:
      #  fileName = fileName.replace('.mp4', '_small.mp4')
    if debug:
      print("Video file name: " + str(fileName))

    fileName = results_dir + "/timelapse_night_" + str(theDate) + ".mp4"

    files = []
    print(imagesDIR + os.sep + "*.jpg")
    for ifile in os.listdir(imagesDIR):
      if ifile.startswith("im") and ifile.endswith(".jpg"):
        files.append(ifile)
    images = sorted(files)
    f = open(imagesDIR + os.sep + 'input.txt', 'w')
    for i in images:
      f.write('file ' + str(i) + '\n')
      print(i)
    f.close()

    if options.scale_down:
      #-f concat -i mylist.txt
      cmd = "ffmpeg -f concat -i " + str(imagesDIR) + os.sep + "input.txt -vf scale=640:480 -framerate 20 -c:v libx264 -pix_fmt yuv420p " + str(fileName)
    else:
      cmd = "ffmpeg -y -f concat -i " + str(imagesDIR) + os.sep + "input.txt -framerate 20 -pattern_type glob -i " + str(imagesDIR) + "\"/image*.jpg\" -c:v libx264 -pix_fmt yuv420p " + str(fileName)
    if debug:
      print(cmd)

    start_time = time.time()
    os.system(cmd)
    end_time = time.time()
    elapsed_time = end_time - start_time
    if debug:
      print("Elapsed time: " + str(elapsed_time) + " s")

    if debug:
      print("Images in: " + str(imagesDIR))
      print("Video file name: " + str(fileName))

    my_file = Path(fileName)
    if my_file.is_file():
      print("Timelapse night video " + str(fileName) + " created. (in " + str(round(elapsed_time,2)) + " s)")
    else:
      print("Timelapse night video " + str(fileName) + " NOT created. (in " + str(round(elapsed_time,2)) + " s)")

  except Exception as e:
    msg = "SkyPi error create timelapse video: " + str(e)
    print(msg)

  sys.exit(0)

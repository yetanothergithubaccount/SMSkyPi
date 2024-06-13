#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Finish the night run, create timelapse video from all the shots of the last night, a startrail, the keograms, etc
#
# Copyright (C) 2021++  Solveigh Matthies
#

import time, datetime
from datetime import date
from datetime import timedelta
import json
import requests
import socket

import optparse
parser = optparse.OptionParser()

from collections import OrderedDict
import os, sys

parser.add_option('-d', '--date',
    action="store", dest="date",
    help="Date")
parser.add_option('-s', '--shutdown',
    action="store_true", dest="shutdown",
    help="No shutdown")

options, args = parser.parse_args()

debug = True #False

########################CONFIG############################
theDate = time.strftime("%Y-%m-%d")
theDateAndTime = time.strftime("%Y-%m-%d_%H-%M-%S")
today = date.today()
yesterday = today - timedelta(days=1)
date_yesterday = yesterday.strftime("%Y-%m-%d")
######################END#CONFIG##########################

if options.date:
  theDate = options.date
  date_yesterday = datetime.datetime.strptime(theDate, '%Y-%m-%d').date() - timedelta(days=1)
  date_yesterday = date_yesterday.strftime("%Y-%m-%d")

def delete_empty_files(rootdir):
  keyword = "~"
  for root, dirs, files in os.walk(rootdir):
    for d in ['RECYCLER', 'RECYCLED']:
      if d in dirs:
        dirs.remove(d)

    for f in files:
      fullname = os.path.join(root, f)
      try:
        if os.path.getsize(fullname) == 0:
          print("Remove empty file: " + str(fullname))
          os.remove(fullname)
        if keyword in fullname: # remove files with ending ~
          print("Remove incomplete file: " + str(fullname))
          os.remove(fullname)
      except Exception as e:
        print("Error removing file: " + str(e))
        continue

#########################MAIN#############################
if __name__ == "__main__":

  state = "START"
  base = "/home/pi/"
  folder = "timelapse_night_" + str(date_yesterday)
  video = "timelapse_night_" + str(date_yesterday) + ".mp4"
  video_small = "small_timelapse_night_" + str(date_yesterday) + ".mp4"
  startrail = "StarTrail_" + str(date_yesterday) + ".jpg"

  try:
    if debug:
      print(state)
      print("SkyPi: Create and mail timelapse video of " + str(date_yesterday) + "..." )

    results_dir = "/home/pi/" + str(date_yesterday)
    if not os.path.exists(results_dir):
      os.makedirs(results_dir)
      if debug:
        print("Directory " + str(results_dir) + " created.")

    state = "STOP"
    if debug:
      print("SkyPi: stop night shot mode. ")
    os.system("/home/pi/skypi/stop.sh")

    # remove empty/incomplete files
    delete_empty_files("timelapse_night_" + str(date_yesterday))

    state = "TIMELAPSE"
    if debug:
      print(state)
      print("Create timelapse video of images of " + str(date_yesterday) + "...")
    start_time = time.time()
    cmd = "python3 /home/pi/skypi/createVideo.py --date " + str(date_yesterday) + " --folder " + str(folder) + " --name " + str(video_small) + " --scale_down"
    if debug:
      print(cmd)
    os.system(cmd)

    end_time = time.time()
    elapsed_time = end_time - start_time
    msg = "Video creation elapsed time: " + str(elapsed_time) + " s"
    if debug:
      print(msg)

    state = "STARTRAIL"
    if debug:
      print(state)
      print("Create startrail of images of " + str(date_yesterday) + "...")
    cmd = "python3 /home/pi/skypi/startrail.py --date " + str(date_yesterday)
    if debug:
      print(cmd)
    os.system(cmd)
    if debug:
      print("Startrail " + str(date_yesterday) + " created.")

    end_time = time.time()
    elapsed_time = end_time - start_time
    if debug:
      print("Video creation elapsed time: " + str(elapsed_time) + " s")
    v = str(base) + os.sep + str(folder) + os.sep + "2" + os.sep + str(video_small)

    state = "KEOGRAM_V"
    if debug:
      print(state)
      print("Create vertical keogram of images of " + str(date_yesterday) + "...")
    if debug:
      print(cmd)
    os.system(cmd)
    cmd = "python3 /home/pi/skypi/keogram.py -d " + str(date_yesterday) + " -v"
    if debug:
      print(cmd)
    os.system(cmd)

    state = "KEOGRAM_H"
    if debug:
      print(state)
    print("Create horizontal keogram of images of " + str(date_yesterday) + "...")
    if debug:
      print(cmd)
    os.system(cmd)
    
    cmd = "python3 /home/pi/skypi/keogram.py -d " + str(date_yesterday) + " -o"
    if debug:
      print(cmd)
    os.system(cmd)

    '''
    try:
      state = "SHARE_RESULTS"
      #TODO send/scp/ftp/etc results somewhere else
    except Exception as e:
      print(e)
    '''

    state = "REVERT_CRONTAB"
    if debug:
      print(state)
    os.system("/home/pi/revert_crontab.sh")

    if options.shutdown:
      state = "SHUTDOWN"
      if debug:
        print(state)
        print("DONE! Shutdown...")
      os.system("sudo shutdown now")
    else:
      if debug:
        print("No shutdown.")
      print("DONE!  Not shutting down.")

  except Exception as e:
    msg = "Skypi finish_night error: " + str(e) + " / " + str(state)
    print(msg)

  sys.exit(0)

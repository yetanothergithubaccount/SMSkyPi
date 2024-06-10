#!/bin/bash
#
# adjust camera via network stream using VLC on remote PC 
#

#ip_address=$(ifconfig | grep 'inet ' | awk '{print $2}')
ip_address=$(hostname -I |  awk '{print $1}')
echo "Open VLC network stream: tcp/h264://$ip_address:3333"

rpicam-vid -t 0 -l -o tcp://0.0.0.0:3333


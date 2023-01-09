#!/bin/bash

docker run \
    --rm \
    --name fill-velocity \
    -e MONITOR_PERIOD=20 \
    -e DRIVE_PREFIX="/dev/sd" \
    -e TZ=America/Edmonton \
    -v /mnt:/opt/disks \
    jconstam/linux-fill-velocity

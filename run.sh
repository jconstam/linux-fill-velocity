#!/bin/bash

docker run \
    --rm \
    --name fill-velocity \
    -e MONITOR_PERIOD=20 \
    -e TZ=America/Edmonton \
    -v /mnt/c:/opt/disks/c \
    -v /mnt/wsl:/opt/disks/wsl \
    jconstam/linux-fill-velocity

#!/bin/bash

docker run \
    --rm \
    --name fill-velocity \
    -e TCP_PORT=12345 \
    -v /mnt/c:/opt/disks/c \
    -v /mnt/wsl:/opt/disks/wsl \
    jconstam/linux-fill-velocity

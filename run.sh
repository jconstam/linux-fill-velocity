#!/bin/bash

docker run \
    --rm \
    --name fill-velocity \
    -v /mnt/c:/opt/disks/c \
    -v /mnt/wsl:/opt/disks/wsl \
    jconstam/linux-fill-velocity

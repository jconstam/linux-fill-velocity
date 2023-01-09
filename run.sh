#!/bin/bash

docker run \
    --rm \
    --name fill-velocity \
    -e TZ=America/Edmonton \
    -e MONITOR_PERIOD=20 \
    -e DRIVE_PREFIX="/dev/sd" \
    -e INFLUXDB_IPADDR="192.168.1.89" \
    -e INFLUXDB_PORT="8086" \
    -e INFLUXDB_USERNAME="root" \
    -e INFLUXDB_PASSWORD="root" \
    -e INFLUXDB_DATABASENAME="drive_data_test" \
    -v /mnt:/opt/disks \
    jconstam/linux-fill-velocity

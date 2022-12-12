#!/bin/sh

if [ -z "${MONITOR_PERIOD}" ]; then
    echo "Monitoring period variable MONITOR_PERIOD must be set."
    exit 1
fi

if [ -z "${TZ}" ]; then
    echo "Timezone environment variable TZ must be set."
    exit 1
fi

TIMEZONE="/usr/share/zoneinfo/${TZ}"
if [ ! -e "${TIMEZONE}" ]; then
    echo "Timezone ${TZ} does not exist."
    exit 1
fi

cp ${TIMEZONE} /etc/localtime
if [ $? -ne 0 ]; then
    echo "Failed to set timezone to ${TZ}".
    exit 1
fi

python3 /opt/fill-velocity.py -p ${MONITOR_PERIOD} /opt/disks/*

#!/bin/bash

check_vars()
{
    var_names=("$@")
    for var_name in "${var_names[@]}"; do
        [ -z "${!var_name}" ] && echo "$var_name is unset." && var_unset=true
    done
    [ -n "$var_unset" ] && exit 1
    return 0
}

check_vars TZ MONITOR_PERIOD DRIVE_PREFIX INFLUXDB_IPADDR INFLUXDB_PORT INFLUXDB_USERNAME INFLUXDB_PASSWORD INFLUXDB_DATABASENAME

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

echo "Ready to run fill-velocity.py"

exit 0

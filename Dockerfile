FROM alpine:3.14

RUN apk add --no-cache bash python3 py3-pip tzdata
RUN pip install --upgrade pip
RUN pip install influxdb

CMD bash /opt/fill-velocity-pre-checks.sh \
    && python3 /opt/fill-velocity.py \
    -p ${MONITOR_PERIOD} \
    -d ${DRIVE_PREFIX} \
    -i ${INFLUXDB_IPADDR} \
    -t ${INFLUXDB_PORT} \
    -u ${INFLUXDB_USERNAME} \
    -w ${INFLUXDB_PASSWORD} \
    -n ${INFLUXDB_DATABASENAME}

COPY ./fill-velocity* /opt/

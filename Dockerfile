FROM alpine:3.14

RUN apk add --no-cache python3 py3-pip tzdata
RUN pip install --upgrade pip

CMD sh /opt/fill-velocity-pre-checks.sh && python3 /opt/fill-velocity.py -p ${MONITOR_PERIOD} -d ${DRIVE_PREFIX}

COPY ./fill-velocity* /opt/

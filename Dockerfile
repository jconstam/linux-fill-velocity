FROM alpine:3.14

RUN apk add --no-cache python3 py3-pip
RUN pip install --upgrade pip

CMD python3 /opt/fill-velocity.py -p ${MONITOR_PERIOD} /opt/disks/*

RUN mkdir -p /opt/disks
COPY ./fill-velocity.py /opt/fill-velocity.py

FROM alpine:3.14

RUN apk add --no-cache python3 py3-pip tzdata
RUN pip install --upgrade pip

CMD sh /opt/fill-velocity.sh

RUN mkdir -p /opt/disks
COPY ./fill-velocity* /opt/

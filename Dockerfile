FROM alpine:3.14

RUN mkdir -p /opt
COPY ./fill-velocity.py /opt/fill-velocity.py

RUN apk add --no-cache python3 py3-pip

CMD python3 /opt/fill-velocity.py

# syntax=docker/dockerfile:1
FROM busybox

RUN mkdir -p /activationBase/

COPY activation_data.csv /activationBase/activation_data.csv
COPY README.md           /activationBase/README.md

CMD ["sh", "-c", "rm -rf /tmp/activationBase/ && mkdir -p /tmp/activationBase/ && cp -r /activationBase/. /tmp/activationBase/"]
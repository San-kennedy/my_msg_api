# Move this file one to level above in directory tree and run build

FROM python:alpine
LABEL maintainer="santosh_ken"

RUN apk add --no-cache bash curl gawk sed grep bc coreutils

RUN pip install gunicorn pymongo falcon

COPY msg_api /opt/msg_api

WORKDIR /opt/msg_api

EXPOSE 8000

ENTRYPOINT ["/usr/local/bin/gunicorn", "-b", "0.0.0.0:8000", "api:MSGAPI"]

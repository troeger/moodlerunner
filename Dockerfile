# Dockerfile for Moodlerunner

FROM alpine

RUN apk update && \
    apk add python3 python3-dev gcc g++ libc-dev make autoconf openjdk8 && \
    rm -rf /var/cache/apk/*

ENV PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/lib/jvm/java-1.8-openjdk/bin"

COPY requirements.txt /
RUN pip3 install -r requirements.txt

COPY moodlerunner.py /

ENTRYPOINT ["/usr/bin/env", "python3", "/moodlerunner.py"]

# Dockerfile for Moodlerunner

FROM ubuntu

ENV LANG en_US.utf8

RUN apt-get update \
    && apt-get install -y locales python3 python3-pip cron gcc make autoconf curl default-jdk \
    && rm -rf /var/lib/apt/lists/* \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8

RUN pip3 install moodleteacher==0.1.8

COPY moodlerunner.py /

ENTRYPOINT ["/usr/bin/env", "python3", "/moodlerunner.py"]

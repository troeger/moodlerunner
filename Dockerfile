# Dockerfile for Moodlerunner

FROM ubuntu

ENV DEBIAN_FRONTEND=noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN=true
ENV LANG en_US.utf8

# Prepare Apache environment
RUN apt-get update \
    && apt-get install -y locales python3 python3-pip vim python3-dev gcc g++ libc-dev make autoconf openjdk-8-jdk \
    && rm -rf /var/lib/apt/lists/* \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8

COPY requirements.txt /
RUN pip3 install -r requirements.txt

COPY moodlerunner.py /

ENTRYPOINT ["/usr/bin/env", "python3", "/moodlerunner.py"]

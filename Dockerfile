# Dockerfile for Moodlerunner

FROM ubuntu

ENV LANG en_US.utf8

RUN apt-get update \
    && apt-get install -y locales python3 python3-pip cron gcc make autoconf curl default-jdk \
    && rm -rf /var/lib/apt/lists/* \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8

RUN    echo "net.ipv6.conf.all.disable_ipv6 = 1\n" >> /etc/sysctl.conf \
    && echo "net.ipv6.conf.default.disable_ipv6 = 1\n" >> /etc/sysctl.conf \
    && echo "net.ipv6.conf.lo.disable_ipv6 = 1\n" >> /etc/sysctl.conf 

RUN pip3 install moodleteacher==0.1.6

COPY moodlerunner.py /

ENTRYPOINT ["/usr/bin/env", "python3", "/moodlerunner.py"]

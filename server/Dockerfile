FROM python:2.7.9
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update
RUN apt-get install -y krb5-config krb5-user
RUN ln -s /usr/bin/krb5-config.mit /usr/bin/krb5-config

ADD requirements.txt /usr/src/app/requirements.txt
RUN pip install -r  /usr/src/app/requirements.txt
ADD . /usr/src/app/

WORKDIR /usr/src/app

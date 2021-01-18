FROM ubuntu:18.04
LABEL maintainer sheiun
RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip
ENV PYTHONUNBUFFERED 1
RUN mkdir /docker_api
WORKDIR /docker_api/
COPY . /docker_api
RUN pip install -r requirements.txt

from ubuntu:20.04
MAINTAINER cb-developer-network@vmware.com

COPY . /app
WORKDIR /app

RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN pip3 install -r requirements.txt
RUN pip3 install .

from amazonlinux:latest
MAINTAINER cb-developer-network@vmware.com

COPY . /app
WORKDIR /app

RUN yum -y install python3-devel
RUN yum -y install python3-pip
RUN pip3 install setuptools
RUN pip3 install -r requirements.txt
RUN pip3 install .

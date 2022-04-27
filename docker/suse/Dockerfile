from opensuse/tumbleweed
MAINTAINER cb-developer-network@vmware.com

COPY . /app
WORKDIR /app

RUN zypper --non-interactive install python3-devel
RUN zypper --non-interactive install python3-pip
RUN zypper --non-interactive install gcc
RUN pip3 install -r requirements.txt
RUN pip3 install .

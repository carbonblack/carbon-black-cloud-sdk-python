FROM opensuse/tumbleweed
LABEL org.opencontainers.image.authors="cb-developer-network@vmware.com"

COPY . /app
WORKDIR /app

RUN zypper --non-interactive install python3-devel
RUN zypper --non-interactive install python3-pip
RUN zypper --non-interactive install gcc

RUN python3 -m venv env
RUN source env/bin/activate

RUN env/bin/pip3 install --break-system-packages -r requirements.txt
RUN env/bin/pip3 install --break-system-packages .

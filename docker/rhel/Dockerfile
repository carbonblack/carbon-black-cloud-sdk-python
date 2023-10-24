FROM registry.access.redhat.com/ubi8/ubi:latest
LABEL org.opencontainers.image.authors="cb-developer-network@vmware.com"

COPY . /app
WORKDIR /app

RUN dnf install -y redhat-rpm-config gcc libffi-devel python38-devel openssl-devel
RUN pip3 install --upgrade pip
RUN pip3 install .[test]

from registry.access.redhat.com/ubi8/ubi:latest
MAINTAINER cb-developer-network@vmware.com

COPY . /app
WORKDIR /app

# https://cryptography.io/en/latest/installation/#fedora-rhel-8-centos-8
RUN yum -y install redhat-rpm-config gcc libffi-devel python-devel openssl-devel

RUN pip3 install -r requirements.txt
RUN pip3 install .

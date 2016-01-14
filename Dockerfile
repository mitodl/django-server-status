FROM python:3.4
MAINTAINER ODL DevOps <mitx-devops@mit.edu>

RUN add-user 
RUN apt-get update
RUN apt-get install -y postgresql-client

RUN adduser --disabled-password --gecos "" mitodl

COPY . /src
WORKDIR /src
RUN chown -R mitodl:mitodl /src

USER mitodl

RUN pip install -r /src/requirements.txt
RUN pip install -r /src/test_requirements.txt

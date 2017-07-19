FROM python:3.6
MAINTAINER ODL DevOps <mitx-devops@mit.edu>

# Add package files
WORKDIR /tmp

# Install base packages
RUN apt-get update
RUN apt-get install -y postgresql-client python-dev python3-dev

# Add non-root user.
RUN adduser --disabled-password --gecos "" mitodl

# Install project packages
COPY requirements.txt /tmp/requirements.txt
COPY test_requirements.txt /tmp/test_requirements.txt

RUN pip install -U pip
RUN pip3 install -U pip
RUN pip install -r requirements.txt -r test_requirements.txt
RUN pip3 install -r requirements.txt -r test_requirements.txt

# Add project
COPY . /src
WORKDIR /src
RUN chown -R mitodl:mitodl /src

RUN apt-get clean && apt-get purge
USER mitodl

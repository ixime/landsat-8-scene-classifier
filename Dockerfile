FROM python:3.6.6

## Environment variables
ARG EEROW
ARG EEPATH
ARG EEDATE
ARG NDVI
ARG CLASSIFY
ARG NESTIMATORS
ARG VALIDATE

## Install requirements
ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

## Copy files
RUN mkdir workspace
WORKDIR /workspace
ADD 01-download 01-download
ADD 02-classification 02-classification
ADD data data
ADD run.sh run.sh

ENTRYPOINT ["/bin/bash", "run.sh"]

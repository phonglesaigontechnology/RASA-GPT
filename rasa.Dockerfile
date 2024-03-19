ARG RASA_VERSION

FROM python:3.8.16

USER root

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    git \
    ca-certificates curl gnupg lsb-release \
    xmlsec1 libxmlsec1-dev

RUN apt-get update
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get install python3.8-dev python3-pip -y

COPY requirements.txt /app/requirements.txt

RUN pip3 install -r requirements.txt
RUN pip3 install rasa-x==0.42.6 --extra-index-url https://pypi.rasa.com/simple/ --use-deprecated=legacy-resolver
RUN pip3 install rasa==2.8.16

USER 1001

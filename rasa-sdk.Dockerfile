ARG RASA_SDK_VERSION
FROM rasa/rasa-sdk:${RASA_SDK_VERSION}

USER root
ENV DEBIAN_FRONTEND noninteractive

WORKDIR /app

RUN apt-get update && apt-get install -y wkhtmltopdf \
    build-essential \
    software-properties-common

COPY sdk-requirements.txt /app/sdk-requirements.txt

RUN pip3 install -r sdk-requirements.txt

USER 1001

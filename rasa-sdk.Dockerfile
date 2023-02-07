ARG RASA_SDK_VERSION
FROM rasa/rasa-sdk:${RASA_SDK_VERSION}

USER root

WORKDIR /app

COPY sdk-requirements.txt /app/sdk-requirements.txt

RUN pip3 install -r sdk-requirements.txt

USER 1001

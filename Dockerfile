FROM ubuntu:20.04
MAINTAINER sic

ENV MINING-ADDRESS=""
ENV RIG-NAME=""
ENV IP-ADDRESS=""
ENV WALLET-ADDY=""
ENV FARM-ID=""
ENV ELECTRIC-COST=""
ENV HIVE-KEY=""
ENV CC-KEY=""
ENV EXPLORER_URL="https://blockchain.info/balance?active="
ENV HIVE_URL="https://api2.hiveos.farm"
ENV CURRENCY=""
ENV BASE_COIN=""
ENV MINING_COIN=""

EXPOSE 9877
EXPOSE 9977
EXPOSE 80

SHELL ["/bin/sh", "-c"]

# Default to supporting utf-8
ENV LANG=C.UTF-8

# Install required packages
RUN apt-get update -q \
    && DEBIAN_FRONTEND=noninteractive apt-get install -yq --no-install-recommends \
      apache2 \
      python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /assets
RUN mkdir /logs

# Copy assets
COPY assets/ /assets/

WORKDIR /assets

RUN pip3 install -r requirements.txt

RUN chmod +x *.py
RUN chmod +x *sh

ENTRYPOINT ["sh", "/assets/run.sh"]

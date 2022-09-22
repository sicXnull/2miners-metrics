FROM ubuntu:20.04
MAINTAINER sic

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
      apache2-utils \
      python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN echo "ServerName localhost" >> /etc/apache2/apache2.conf
RUN service apache2 restart

RUN mkdir /assets
RUN mkdir /logs

# Copy assets
COPY assets/ /assets/

WORKDIR /assets

RUN pip3 install -r requirements.txt

RUN chmod +x *.py
RUN chmod +x *.sh

ENTRYPOINT ["sh", "/assets/run.sh"]

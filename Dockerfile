FROM phusion/baseimage:0.9.11

# Dependencies
RUN DEBIAN_FRONTEND='noninteractive' \
  apt-get update && \
  apt-get -y --force-yes install python-pip python-dev build-essential \
    software-properties-common python-software-properties libpq-dev \
    binutils libproj-dev gdal-bin

# Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN useradd -m -d /srv/addressfinder addressfinder

ADD . /srv/addressfinder
RUN rm -rf /srv/tribunals/.git
RUN chown -R addressfinder: /srv/addressfinder
RUN su - addressfinder -c "pip install -r requirements.txt"

EXPOSE 8000
USER addressfinder
WORKDIR /srv/addressfinder

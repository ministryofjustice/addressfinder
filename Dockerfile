# Pull base image.
FROM phusion/baseimage:0.9.11

MAINTAINER Kerin Cosford <kerin.cosford@digital.justice.gov.uk>

# Set correct environment variables.
ENV HOME /root

# Use baseimage-docker's init process.
CMD ["/sbin/my_init"]

# Set timezone
RUN echo "Europe/London" > /etc/timezone  &&  dpkg-reconfigure -f noninteractive tzdata

# Dependencies
RUN DEBIAN_FRONTEND='noninteractive' \
  apt-get update && \
  apt-get -y --force-yes install python-pip python-dev build-essential git \
    software-properties-common python-software-properties libpq-dev \
    binutils libproj-dev gdal-bin

# Install Nginx.
RUN DEBIAN_FRONTEND='noninteractive' add-apt-repository ppa:nginx/stable && apt-get update
RUN DEBIAN_FRONTEND='noninteractive' apt-get -y --force-yes install nginx-full && \
    chown -R www-data:www-data /var/lib/nginx

ADD ./docker/nginx.conf /etc/nginx/nginx.conf
RUN rm -f /etc/nginx/sites-enabled/default

RUN mkdir -p /var/log/wsgi && touch /var/log/wsgi/app.log /var/log/wsgi/debug.log && \
    chown -R www-data:www-data /var/log/wsgi && chmod -R g+s /var/log/wsgi

RUN  mkdir -p /var/log/nginx/addressfinder
ADD ./docker/addressfinder.ini /etc/wsgi/conf.d/addressfinder.ini

# Define mountable directories.
VOLUME ["/var/log/nginx", "/var/log/wsgi"]

# APP_HOME
ENV APP_HOME /home/app/django

# Add project directory to docker
ADD . /home/app/django

# PIP INSTALL APPLICATION
RUN cd /home/app/django && \
    pip install -r requirements.txt && \
    find . -name '*.pyc' -delete

# install service files for runit
ADD ./docker/nginx.service /etc/service/nginx/run
RUN chmod +x /etc/service/nginx/run

# install service files for runit
ADD ./docker/uwsgi.service /etc/service/uwsgi/run
RUN chmod +x /etc/service/uwsgi/run

# Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Expose ports.
EXPOSE 80

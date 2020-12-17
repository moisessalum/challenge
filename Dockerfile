FROM ubuntu:18.04

LABEL maintainer="Moises Salum <moises.rodriguez.salum@gmail.com>"

# update ubuntu
RUN apt-get update && apt-get upgrade -y

# install wget, gnupg and systemd
RUN apt-get install -y wget \
  && apt-get install -y gnupg \
  && apt-get install -y systemd

# import repository signing key for psql & mongodb
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
RUN echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.4 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-4.4.list
RUN wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | apt-key add -

# install psql, mongo, pip3, pymongo
RUN apt-get -y install postgresql \
  && apt-get -y install mongodb \
  && apt-get -y install python3-pip \
  && apt-get -y install python-psycopg2 \
  && apt-get -y install libpq-dev \
  && pip3 install --upgrade pip

# copy psql, mongo & requirements files
COPY psql_transactional.sql /tmp/psql_transactional.sql
COPY psql_analytical.sql /tmp/psql_analytical.sql
COPY mongo_transactional.py /tmp/mongo_transactional.py
COPY requirements.txt /tmp/requirements.txt
COPY .env_vars /.env_vars
COPY etl.py /etl.py

# run psql_transactional script
USER postgres
RUN /etc/init.d/postgresql start \
  && psql -f /tmp/psql_transactional.sql \
  && psql -f /tmp/psql_analytical.sql

# install pymongo and run script
USER root
RUN pip3 install -r /tmp/requirements.txt
RUN /etc/init.d/mongodb start && python3 /tmp/mongo_transactional.py

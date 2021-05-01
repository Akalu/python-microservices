# This Dockerfile is for localdev purposes only, so it won't be
# optimised for size
FROM alpine:3.9

# Add the proper env variables for init the db
ARG POSTGRES_DB
ENV POSTGRES_DB $POSTGRES_DB
ARG POSTGRES_USER
ENV POSTGRES_USER $POSTGRES_USER
ARG POSTGRES_PASSWORD
ENV POSTGRES_PASSWORD $POSTGRES_PASSWORD
ARG POSTGRES_PORT
ENV LANG en_US.utf8
EXPOSE $POSTGRES_PORT

# For usage in startup, etc
ENV POSTGRES_HOST localhost
ENV DATABASE_ENGINE POSTGRESQL
# Store the data inside the container, as we don't care for
# persistence
RUN mkdir -p /opt/data
ENV PGDATA /opt/data

RUN apk update
RUN apk add bash curl su-exec python3
RUN apk add postgresql postgresql-contrib postgresql-dev
RUN apk add python3-dev build-base linux-headers gcc libffi-dev

# Adding our code
WORKDIR /opt/code

RUN mkdir -p /opt/code/db
# Add postgres setup
ADD ./docker_pg/db/postgres-setup.sh /opt/code/db/postgres-setup.sh

# Make script executable
RUN chmod +x /opt/code/db/postgres-setup.sh
RUN  ./db/postgres-setup.sh

## Install code to prepare the DB
ADD ./nanotwitter_pg/requirements.txt /opt/code/requirements.txt

RUN pip3 install -r requirements.txt

## Need to import all the code, due to dependencies to initialise the DB
ADD ./nanotwitter_pg/ /opt/code/nanotwitter_pg/

# Add all DB commands
ADD ./docker_pg/db/* /opt/code/db/

## get the db ready
RUN /opt/code/db/prepare_db.sh

# Start the database in normal operation
USER postgres
CMD ["postgres"]

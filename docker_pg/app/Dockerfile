########
# This image will compile the dependencies
# It will install compilers and other packages, that won't be carried
# over to the runtime image
########
FROM alpine:3.9 AS compile-image

# Add requirements for python and pip
RUN apk add --update python3

# NOTE: base directory will be /opt/code, but the source code of server will in enclosed directory
# this was done due to complex structure of directories in current project
# and necessity to test code locally before moving into production
# For real production services the best practice will be to put the source code of each
# microservice into separate directory

RUN mkdir -p /opt/code
RUN mkdir -p /opt/code/nanotwitter_pg
WORKDIR /opt/code

# Install dependencies
RUN apk add python3-dev build-base gcc linux-headers postgresql-dev libffi-dev

# Create a virtual environment for all the Python dependencies
RUN python3 -m venv /opt/venv
# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"
RUN pip3 install --upgrade pip

# Install and compile uwsgi
RUN pip3 install uwsgi==2.0.18

# Install other dependencies
COPY ./nanotwitter_pg/requirements.txt /opt/requirements.txt
RUN pip3 install -r /opt/requirements.txt

########
# This image is the runtime, will copy the dependencies from the other
########
FROM alpine:3.9 AS runtime-image

# Install python
RUN apk add --update python3 curl libffi postgresql-libs

# Copy uWSGI configuration into separate directory
RUN mkdir -p /opt/uwsgi
ADD docker_pg/app/uwsgi.ini /opt/uwsgi/
ADD docker_pg/app/start_server.sh /opt/uwsgi/

# Create a user to run the service
RUN addgroup -S uwsgi
RUN adduser -H -D -S uwsgi
USER uwsgi

# Copy the venv with compile dependencies from the compile-image
COPY --chown=uwsgi:uwsgi --from=compile-image /opt/venv /opt/venv
# Be sure to activate the venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy the code
COPY --chown=uwsgi:uwsgi nanotwitter_pg/ /opt/code/nanotwitter_pg/

# Run parameters
WORKDIR /opt/code
EXPOSE 5000
CMD ["/bin/sh", "/opt/uwsgi/start_server.sh"]

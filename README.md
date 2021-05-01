RESTful Python microservice
=============================

This code is an example of RESTful service web app. 

It is a Flask application (https://www.djangoproject.com/) that creates a RESTful backend to store user's posts. In other 
words it's a nano-twitter application

Overview
=========
The format of a Tweet POJO is as follows:

```
{
    id integer
    username string
    text string
    timestamp string($date-time)
}
```

API has the following contract:


public api:

| Method | Endpoint                   |Secure|      Description                               |
|--------|----------------------------|------|------------------------------------------------|
|GET     |  /api/me/tweets/           |  Yes |    List of tweets of the user                  |
|POST    |  /api/me/tweets/           |  Yes |    The newly created tweet                     |
|GET     |  /api/tweets/              |  No  |    List of all tweets                          |
|GET     |  /api/tweets/{id}/         |  No  |    The tweet with ID=id                        |  
|GET     |  /api/tweets/?search=token |  No  |    Searches all the tweets that contain token  |


private api:

Method  Endpoint                Secure      Description

DELETE  /admin/tweets/{id}/         No      Deletes tweet with ID=id

Database has the following schema (created through SQLAlchemy https://www.sqlalchemy.org/):

id INTEGER NOT NULL Primary key
username VARCHAR(50)
text VARCHAR(250)
timestamp DATETIME Creation time

Build and run local service - nanotwitter
==========================================


Create a virtual environment and install the requirements

```
python3 -m venv ./venv
source ./venv/bin/activate OR .\venv\Scripts\activate
pip install -r requirements.txt
```

Get the local database ready

```
python -m nanotwitter.init_db
```

Generate the API token:
```
python -m nanotwitter.gen_token
Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaWF0IjoxNjE5ODUxNzI4LCJleHAiOjE2MjAwMjQ1Mjh9.BAt0K-_c_MqF1i1ZjHYseXl9lg4Vrs8gxlD1PDszIgJz3i-l-ahbzJgEbw6Fs65gNGezqb40bm1wH4znBfmrpO6l3OPSvE3Sbmm0b-_umZNfNWz4cpg
2Cp9p9dmqlcStSqd_JuCwPKHbrVCPyExmUOfGrEugDXh8A0ZOGlzllU7XRGaQyQXvRn_BzvmH_q8NgTTksizRMXW_Jj3-bMnuVxuzmQNwTCPni_P9Yu9ptppLsG2GoJhtOPNH76TPjK4sl9fIPKchDC54ELDd0jDMuTbaoNRYcyXl2cv14o6VZ-mK_w1vcjETQD_izQIpq4CiwFllHQGYVCnAAo4kLXO8Fg
```

Start the development server

```
set FLASK_APP=.\nanotwitter\wsgi.py 
set FLASK_ENV=development

flask run
```

Check the service at http://127.0.0.1:5000/

Build and run dockerized microservice - nanotwitter_pg
=======================================================

Note, there are tiny differences between nanotwitter_pg and nanotwitter_pg - in a way of working with DB layer and in
dependencies

Use this command to build and spin up containers:

```
docker-compose -f docker-compose-pg.yaml up --build
```

and this one to destroy them:

```
docker-compose -f docker-compose-pg.yaml down
```
Check the service at http://127.0.0.1:5000/

Tests
======

Run the unit tests with

```
pytest
```

Dependencies
=============

This application uses:

* Flask as a web framework ()
  
* Flask RESTplus for creating the web interface, similar to Swagger (https://flask-restplus.readthedocs.io/en/stable)

* SQLAlchemy to handle the database models (https://www.sqlalchemy.org/)

* SQLlite database for local development and U-tests ()

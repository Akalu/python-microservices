from flask import Flask
from flask_restplus import Api


def create_app():
    from nanotwitter_pg.backend.api_namespace import api_namespace
    from nanotwitter_pg.backend.admin_namespace import admin_namespace

    application = Flask(__name__)
    api = Api(application, version='0.0.1', title='Simple Nanotwitter Backend API',
              description='A Simple CRUD API')

    from nanotwitter_pg.backend.db import db, db_config
    application.config['RESTPLUS_MASK_SWAGGER'] = False
    application.config.update(db_config)
    db.init_app(application)
    application.db = db

    api.add_namespace(api_namespace)
    api.add_namespace(admin_namespace)

    return application

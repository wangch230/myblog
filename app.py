from flask import Flask
from ext import db, bootstrap
from settings import config


def create_app(config_name=None):

    if config_name is None:
        config_name = 'development'

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    bootstrap.init_app(app)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()

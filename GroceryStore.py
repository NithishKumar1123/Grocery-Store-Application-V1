import os
from flask import Flask
from application.database import db
from application import config
from application.config import LocalDevelopmentConfig

app = None

def create_app():
    app = Flask(__name__, template_folder = 'templates')
    if(os.getenv('ENV', "development") == "production"):
        raise Exception("Currently no production config is setup.")
    else:
        print("Starting Local Development")
        app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    app.app_context().push()
    return app

app = create_app()

from controllers.admin_controller import *
from controllers.user_controller import *
from controllers.controller import *

if __name__ == '__main__':
    app.run()
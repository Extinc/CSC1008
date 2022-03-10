from flask import Flask
from sqlalchemy import event
from App.settings.config import config_
from .extension import db, login_manager
from App.routes import *
from App.model.UserDB import User
# initialize extensions
# spatialite_path = 'addon/mod_spatialite.dylib'
# os.environ['PATH'] = spatialite_path + ';' + os.environ['PATH']

# app factory
def create_app(config_name = "default"):
    # create app instance
    app = Flask(__name__, template_folder="templates", static_folder = "static")
    app.create_jinja_environment()
    # configure app
    app.config.from_object(config_[config_name])

    # initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(routes)

    with app.app_context():
        @event.listens_for(db.engine, "connect")
        def load_spatialite(dbapi_conn, connection_record):
            dbapi_conn.enable_load_extension(True)
            dbapi_conn.load_extension('App/addon/mod_spatialite.dylib')
        db.create_all()
        return app
from flask import Flask
from sqlalchemy import event


from App.settings.config import config_
from .extension import db
from App.routes import *
# initialize extensions
# spatialite_path = 'addon/mod_spatialite.dylib'
# os.environ['PATH'] = spatialite_path + ';' + os.environ['PATH']

# app factory
def create_app(config_name = "default"):
    # create app instance
    app = Flask(__name__)

    # configure app
    app.config.from_object(config_[config_name])

    # initialize extensions
    db.init_app(app)


    app.register_blueprint(routes)
    with app.app_context():
        @event.listens_for(db.engine, "connect")
        def load_spatialite(dbapi_conn, connection_record):
            dbapi_conn.enable_load_extension(True)
            dbapi_conn.load_extension('App/addon/mod_spatialite.dylib')
        return app
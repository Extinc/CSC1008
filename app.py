from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.event import listen
from sqlalchemy.sql import select, func
from sqlalchemy.orm import sessionmaker
from backend.models import dbstore
import folium
import os.path
app = Flask(__name__)
print(os.path.exists("/opt/homebrew/Cellar/libspatialite/5.0.1_1/lib/mod_spatialite.dylib"))
def load_spatialite(dbapi_conn, connection_record):
    dbapi_conn.enable_load_extension(True)
    dbapi_conn.load_extension("./addon/mod_spatialite.dylib")

engine = create_engine('sqlite:///backend/db1.sqlite', echo=True)
listen(engine, 'connect', load_spatialite)
conn = engine.connect()

# conn.execute(select([func.InitSpatialMetaData()]))

Session = sessionmaker(bind=engine)
session = Session()


query = session.query(dbstore.Waterways).order_by(dbstore.Waterways.osm_id)
# waterways_free_1.geometry
for data in query:
    print(data.geometry.ST_AsGeoJSON())

@app.route('/')
def index():  # put application's code here

    return render_template("index.html")


@app.route('/map')
def Map():  # put application's code here
    my_map = folium.Map(location=[1.4299797559324452,103.8286492616571], zoom_start=13)
    return render_template("map.html")


if __name__ == '__main__':
    app.run(debug=True)

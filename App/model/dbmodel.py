from App.extension import db
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2 import Geometry
from sqlalchemy import Column, Integer, String
from App.settings.config import Config

base = declarative_base()



# For Account
class User(base, db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

# For Map

class Roads(base):
    __tablename__ = 'SG_Points'
    pk_uid = db.Column(db.Integer, primary_key=True)
    osm_id = db.Column(String)
    operator = db.Column(Integer)
    ref = db.Column(String)
    oneway = db.Column(String)
    maxspeed = db.Column(Integer)
    layer = db.Column(Integer)
    bridge = db.Column(String)
    tunnel = db.Column(String)
    geometry = db.Column(Geometry('POINT', srid=Config.MAP_SRID))

class RoadLine(base):
    __tablename__ = 'Road_lines'
    pk_uid = db.Column(Integer, primary_key=True)
    osm_id = db.Column(String)
    ref = db.Column(String)
    oneway = db.Column(String)
    maxspeed = db.Column(Integer)
    layer = Column(Integer)
    bridge = db.Column(String)
    tunnel = db.Column(String)
    geometry = db.Column(Geometry('LINESTRING', srid=Config.MAP_SRID))

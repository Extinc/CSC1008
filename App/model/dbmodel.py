from App.extension import db
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2 import Geometry
from sqlalchemy import Column, Integer, String
from App.settings.config import Config

base = declarative_base()

# For Map

class Roads(base, db.Model):
    __tablename__ = 'SG_Points'
    pk_uid = db.Column(db.Integer, primary_key=True)
    osm_id = db.Column(db.String)
    operator = db.Column(db.Integer)
    ref = db.Column(db.String)
    oneway = db.Column(db.String)
    maxspeed = db.Column(db.Integer)
    layer = db.Column(db.Integer)
    bridge = db.Column(db.String)
    tunnel = db.Column(db.String)
    geometry = db.Column(Geometry(geometry_type='POINT', srid=Config.MAP_SRID))

class RoadLine(base, db.Model):
    __tablename__ = 'Road_lines'
    pk_uid = db.Column(Integer, primary_key=True)
    osm_id = db.Column(db.String)
    ref = db.Column(db.String)
    oneway = db.Column(db.String)
    maxspeed = db.Column(db.Integer)
    layer = Column(db.Integer)
    bridge = db.Column(db.String)
    tunnel = db.Column(db.String)
    geometry = db.Column(Geometry(geometry_type='LINESTRING', srid=Config.MAP_SRID))

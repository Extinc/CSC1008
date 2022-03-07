from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2 import Geometry
from sqlalchemy import create_engine, Column, Integer, String

base = declarative_base()

srid = 4326

class Waterways(base):
    __tablename__ = 'waterways'
    pk_uid = Column(Integer, primary_key=True)
    osm_id = Column(String)
    code = Column(Integer)
    fclass = Column(String)
    width = Column(Integer)
    name = Column(String)
    geometry = Column(Geometry('LINESTRING', srid=srid))

class Roads(base):
    __tablename__ = 'roads'
    pk_uid = Column(Integer, primary_key=True)
    osm_id = Column(String)
    code = Column(Integer)
    fclass = Column(String)
    name = Column(String)
    ref = Column(String)
    oneway = Column(String)
    maxspeed = Column(Integer)
    layer = Column(Integer)
    bridge = Column(String)
    tunnel = Column(String)
    geometry = Column(Geometry('LINESTRING', srid=srid))
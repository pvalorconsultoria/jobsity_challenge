from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

Base = declarative_base()

class BaseTrip(Base):
    __tablename__ = 'trips'
    id = Column(Integer, primary_key=True)
    region = Column(String(50))
    origin_x = Column(Float())
    origin_y = Column(Float())
    destination_x = Column(Float())
    destination_y = Column(Float())
    datasource = Column(String(100))

class Trip(db.Model):
    __tablename__ = 'trips'
    id = db.Column(db.Integer, primary_key=True)
    region = db.Column(db.String(50))
    origin_x = db.Column(db.Float())
    origin_y = db.Column(db.Float())
    destination_x = db.Column(db.Float())
    destination_y = db.Column(db.Float())
    datasource = db.Column(db.String(100))

    def to_dict(self):
        return {
            'id': self.id,
            'region': self.region,
            'origin_x': self.origin_x,
            'origin_y': self.origin_y,
            'destination_x': self.destination_x,
            'destination_y': self.destination_y,
            'datasource': self.datasource
        }
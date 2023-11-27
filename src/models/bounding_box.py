from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float

Base = declarative_base()

class BoundingBox(Base):
    __tablename__ = 'bounding_boxes'
    id = Column(Integer, primary_key=True)
    x_min = Column(Float())
    y_min = Column(Float())
    x_max = Column(Float())
    y_max = Column(Float())

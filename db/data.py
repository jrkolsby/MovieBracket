from sqlalchemy import Boolean, Integer, String
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy import create_engine, MetaData, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

engine = create_engine('sqlite:///db/awards.db', echo=True)
session = sessionmaker(bind=engine)()
metaData = MetaData()

Base = declarative_base(metadata=metaData)

class Movie(Base):
    __tablename__ = 'movies'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String)

    def __init__(self, name, entity):
        self.name = award 
        self.entity = entity

class Award(Base):
    __tablename__ = 'awards'

    id = Column('id', Integer, primary_key=True)
    entity = Column('entity', String)
    name = Column('name', String)

    def __init__(self, name, entity):
        self.name = award 
        self.entity = movie

class Join(Base):
    __tablename__ = 'join'

    movie = Column('movie', Integer, ForeignKey('movies.id'), primary_key=True) 
    award = Column('award', Integer, ForeignKey('awards.id'), primary_key=True)

    def __init__(self, movie, award):
        self.movie = movie
        self.award = award 
    
# CREATE tables
metaData.create_all(engine)

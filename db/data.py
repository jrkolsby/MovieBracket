import os

from sqlalchemy import Boolean, Integer, String
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy import create_engine, MetaData, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

cwd = os.path.dirname(os.path.realpath(__file__)) 

engine = create_engine('sqlite:///' + cwd + '/awards.db', echo=True)
session = sessionmaker(bind=engine)()
metaData = MetaData()

Base = declarative_base(metadata=metaData)

class Movie(Base):
    __tablename__ = 'movies'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String)

    def __init__(self, name):
        self.name = name

class Award(Base):
    __tablename__ = 'awards'

    id = Column('id', Integer, primary_key=True)
    entity = Column('entity', String)
    name = Column('name', String)
    win = Column('win', Boolean)

    def __init__(self, entity, name, win):
        self.win = win
        self.name = name
        self.entity = entity

class Join(Base):
    __tablename__ = 'join'

    movie = Column('movie', Integer, ForeignKey('movies.id'), primary_key=True) 
    award = Column('award', Integer, ForeignKey('awards.id'), primary_key=True)

    def __init__(self, movie, award):
        self.movie = movie
        self.award = award
    
# CREATE tables
metaData.create_all(engine)

# returns ID
def createMovie(name):
    movie = Movie(name)
    session.add(movie)
    session.flush()
    session.commit()

    return movie.id

def createAward(entity, name, win):
    award = Award(entity, name, win)
    session.add(award)
    session.flush()
    session.commit()

    return award.id 

def createJoin(movie, award):
    join = Join(movie, award)
    session.add(join)
    session.flush()
    session.commit()

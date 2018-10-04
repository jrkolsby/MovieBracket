import os

from sqlalchemy import Boolean, Integer, String
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy import create_engine, MetaData, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.orm.exc import NoResultFound

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
    movie = findMovie(name) 

    if movie is None:
        movie = Movie(name)
        session.add(movie)
        session.flush()
        session.commit()

    return movie

def createAward(entity, name, win):
    
    award = findAward(entity, name, win) 

    if award is None:
        award = Award(entity, name, win)
        session.add(award)
        session.flush()
        session.commit()

    return award

def createJoin(movie, award):

    join = findJoin(movie.id, award.id);

    if join is None:
        join = Join(movie.id, award.id)
        session.add(join)
        session.flush()
        session.commit()

    return join

def findAward(entity=None, name=None, win=None):

    entityFilter = nameFilter = winFilter = (True)

    if entity is not None:
        entityFilter = (Award.entity.like("%"+entity+"%"))

    if name is not None:
        nameFilter = (Award.name.like("%"+name+"%"))

    if win is not None:
        winFilter = (Award.win == win)

    return session.query(Award) \
        .filter(entityFilter) \
        .filter(nameFilter) \
        .filter(winFilter).first()

def findMovie(name=None):

    nameFilter = (True)

    if name is not None:
        nameFilter = Movie.name.like("%"+name+"%");

    return session.query(Movie) \
        .filter(nameFilter).first()

def findJoin(movie=None, award=None):

    movieFilter = awardFilter = (True)

    if movieFilter is not None:
        movieFilter = (Join.movie == movie)

    if awardFilter is not None:
        awardFilter = (Join.award == award)

    return session.query(Movie) \
        .filter(movieFilter) \
        .filter(awardFilter).first()

def getAwards(movieName):
    movie = findMovie(name=movieName)

    if movie is None:
        return []

    joins = session.query(Join) \
        .filter(Join.movie == movie.id).all()

    if joins is None:
        return []

    return list(map(lambda j: \
        session.query(Award).get(j.award), joins))      

def compareMovies(a, b):
    movieA = findMovie(name=a)
    movieB = findMovie(name=b)
    print("a: " + movieA.name)
    print("a: " + movieB.name)

    return movieA

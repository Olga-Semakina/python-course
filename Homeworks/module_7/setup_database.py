from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

db_name = 'films_db'
engine = create_engine("sqlite:///{}.db".format(db_name), echo=True)

Base = declarative_base()


class Film(Base):
    __tablename__ = "films"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    director = Column(String)
    release_year = Column(Integer)


Base.metadata.create_all(engine)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from setup_database import Film
from setup_database import db_name

engine = create_engine("sqlite:///{}.db".format(db_name), echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# add 3 films to the table
films = [Film(title='The Lord of the Rings', director='Peter Jackson', release_year='2003'),
         Film(title='The Dark Knight', director='Christopher Nolan', release_year='2008'),
         Film(title='Pulp Fiction', director='Quentin Tarantino', release_year='1990')]
for film in films:
    session.add(film)
session.commit()

# update the entry in the table
films[2].release_year = '1994'
session.commit()

# print data
inserted_films = session.query(Film).all()
for film in inserted_films:
    print(film.id, film.title, film.director, film.release_year)

# delete data
for film in inserted_films:
    session.delete(film)
session.commit()

# close session
session.close()

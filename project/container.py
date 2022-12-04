"""This unit contains  an instances of DAOs and Services"""
from project.dao import GenresDAO, DirectorDao, MovieDao, UserDao, FavoritesDAO
from project.services import DirectorService, MovieService, UserService, \
    FavoritesService
from project.services import GenreService, AuthService
from project.setup.db import db
# ------------------------------------------------------------------------
# DAO
genre_dao = GenresDAO(db.session)
director_dao = DirectorDao(db.session)
movie_dao = MovieDao(db.session)
user_dao = UserDao(db.session)
favorite_dao = FavoritesDAO(db.session)

# Services
genre_service = GenreService(dao=genre_dao)
director_service = DirectorService(dao=director_dao)
movie_service = MovieService(dao=movie_dao)
auth_service = AuthService(dao=user_dao)
user_service = UserService(dao=user_dao)
favorite_service = FavoritesService(dao=favorite_dao)

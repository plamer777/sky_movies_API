"""This unit contains a FavoritesDAO class to work with user_movie table"""
from typing import List

from project.dao.base import BaseDAO
from project.models import UserMovie
# --------------------------------------------------------------------------


class FavoritesDAO(BaseDAO[UserMovie]):
    """The FavoritesDAO class provides necessary methods using to get data
    from user_movie table"""
    __model__ = UserMovie

    def get_by_user_id(self, user_id: int) -> List[UserMovie]:
        """This method returns a single user by id

        :param user_id: the id of the user

        :return: a model representing the user
        """

        return self._db_session.query(UserMovie).filter(
            UserMovie.user_id == user_id).all()

    def get_by_user_and_movie(self, d_movie: dict) -> UserMovie:
        """This method returns all records found by user_id and movie_id

        :param d_movie: a dictionary with user_id and movie_id

        :return: a list of models representing the requested records
        """
        found = self.__model__.query.filter(
            UserMovie.movie_id == d_movie.get('movie_id'),
            UserMovie.user_id == d_movie.get('user_id')).first()

        return found

    def add_new(self, d_movie: dict) -> UserMovie:
        """This method adds a new record to the user_movie table

        :param d_movie: a dictionary with user_id and movie_id

        :return: a model representing the added record
        """
        user_movie = UserMovie(**d_movie)

        self._db_session.add(user_movie)
        self._db_session.commit()

        return user_movie

    def delete(self, d_movie: dict) -> None:
        """This method deletes a record from the user_movie table

        :param d_movie: a dictionary with user_id and movie_id
        """
        self.__model__.query.filter(UserMovie.movie_id == d_movie.get(
            'movie_id'), UserMovie.user_id == d_movie.get('user_id')).delete()

        self._db_session.commit()

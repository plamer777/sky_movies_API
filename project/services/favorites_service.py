"""The unit contains a FavoritesService class with business logic for
user_movie table of the database"""
from typing import List, Tuple
from flask import abort
from project.models import UserMovie
from project.services.base import BaseService
from project.dao import FavoritesDAO
# -------------------------------------------------------------------------


class FavoritesService(BaseService[FavoritesDAO]):
    """The FavoritesService class provides a business logic to add/remove
    movies to/from favorites"""

    def get_by_user_id(self, user_id: int) -> List[UserMovie]:

        found = self.dao.get_by_user_id(user_id)

        if not found:
            abort(404, f"User with id {user_id} is not found")

        return found

    def add(self, d_movie: dict) -> Tuple[UserMovie, int]:
        """The method serves the add a new favorite movie to the user_movie
        table

        :param d_movie: a dictionary with data to add

        :returns: a tuple with added model and calculated id of favorite
        user's genre
        """
        try:
            if self.dao.get_by_user_and_movie(d_movie):
                abort(400, 'Already exists')

            added = self.dao.add_new(d_movie)

            favorites = self.get_by_user_id(d_movie.get('user_id'))

            fav_genre_id = self._get_favorite_genre_id(favorites)

            return added, fav_genre_id

        except Exception as e:

            print(f'При добавлении фильма в избранные возникла ошибка {e}')
            abort(400, 'Bad request')

    def remove(self, d_movie: dict) -> None:
        """The method serves the remove a record from the user_movie table

        :param d_movie: a dictionary with user_id and movie_id
        """
        try:

            self.dao.delete(d_movie)

        except Exception as e:

            print(f'При удалении фильма из избранных возникла ошибка {e}')
            abort(404, 'Not Found')

    @staticmethod
    def _get_favorite_genre_id(favorites: List[UserMovie]) -> int:
        """This is a secondary method to calculate id of the most popular
        user's movies genre

        :param favorites: a list of movies added to the favorites

        :returns: the id of the most popular user's genre'
        """
        genre_counter = {}

        for favorite in favorites:

            genre_counter.setdefault(favorite.movie.genre_id, 0)
            genre_counter[favorite.movie.genre_id] += 1

        return max(genre_counter, key=lambda x: genre_counter[x])

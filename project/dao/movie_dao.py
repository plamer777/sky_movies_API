"""This unit contains a MovieDao class to work with movies table"""
from typing import Optional, List

from sqlalchemy import desc
from werkzeug.exceptions import NotFound

from project.dao.base import BaseDAO, T
from project.models import Movie
# ------------------------------------------------------------------------


class MovieDao(BaseDAO[Movie]):
    """The MovieDao class provides necessary methods to get data from the
    'movies' table"""
    __model__ = Movie

    def get_all(self, page: Optional[int] = None, status: str = None) -> \
            List[T]:
        """This method returns a list of movies found in a certain table

        :param page: an optional parameter for page number to sort items by
        :param status: a string, if status = 'new' then movies will be sorted
        by the year from freshest to oldest

        :return: a list of models representing the items
        """
        if status == 'new':
            query = self._db_session.query(self.__model__).order_by(desc(
                self.__model__.year))

        else:
            query = self._db_session.query(self.__model__)

        if page:
            try:
                movies = query.paginate(page=page,
                                        per_page=self._items_per_page).items
                return movies

            except NotFound:
                return []

        return query.all()

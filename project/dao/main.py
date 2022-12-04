"""The unit contains a GenreDAO class to work the 'genres' table"""
from project.dao.base import BaseDAO
from project.models import Genre
# ---------------------------------------------------------------------------


class GenresDAO(BaseDAO[Genre]):
    """The GenreDAO class provides necessary methods to get data from the
    'genres' table"""
    __model__ = Genre

"""The unit contains a GenreService class with business logic for genres
table of the database"""
from project.services.base import BaseService
from project.dao import GenresDAO
# ------------------------------------------------------------------------


class GenreService(BaseService[GenresDAO]):
    """The GenreService class provides a business logic to work with genre
    table"""
    pass

"""The unit contains a DirectorDao class to work the 'directors' table"""
from project.dao.base import BaseDAO
from project.models import Director
# -----------------------------------------------------------------------


class DirectorDao(BaseDAO[Director]):
    """The DirectorDao class provides necessary methods to get data from the
    'directors' table"""
    __model__ = Director

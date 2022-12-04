"""The unit contains a MovieService class with business logic to get data
from movies table"""
from typing import Optional, List

from flask_sqlalchemy import Model

from project.services.base import BaseService
from project.dao import MovieDao
# ------------------------------------------------------------------------


class MovieService(BaseService[MovieDao]):
    """The MovieService clss provides a business logic to process user's
    requests regarding certain table"""

    def get_all(self, page: Optional[int] = None, status: str = None) -> \
            List[Model]:
        """The method returns a list of models found in the table. All
        records will be paginated if 'page' is specified

        :param page: a requested page number
        :param status: a string. If the string = 'new' then all records will
        be sorted by year from newest to oldest

        :returns: a list of models
        """

        return self.dao.get_all(page=page, status=status)

"""The unit contains a BaseService class with basic logic to be inherited by
another classes"""
from typing import Optional, List, TypeVar, Generic
from flask_sqlalchemy import Model
from project.dao.base import BaseDAO
from project.exceptions import ItemNotFound
# ------------------------------------------------------------------------
T = TypeVar('T', bound=BaseDAO)
# ------------------------------------------------------------------------


class BaseService(Generic[T]):
    """The BaseService clss provides a business logic to process user's
    requests regarding certain table"""

    def __init__(self, dao: Optional[T]) -> None:
        """The initialization of the class

        :param dao: an instance of DAO class
        """
        self.dao: Optional[T] = dao

    def get_item(self, pk: int) -> Model:
        """This method returns a single record by provided pk

        :param pk: the id of searching record

        :returns: a model with requested data
        """
        if record := self.dao.get_by_id(pk):
            return record
        raise ItemNotFound(f'Record with pk={pk} not exists.')

    def get_all(self, page: Optional[int] = None) -> List[Model]:
        """The method returns a list of models found in the table. All
        records will be paginated if 'page' is specified

        :param page: a requested page number

        :returns: a list of models
        """
        return self.dao.get_all(page=page)

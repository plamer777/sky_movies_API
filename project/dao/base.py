"""This unit contains a BaseDAO class to inherit by another classes"""
from typing import Generic, List, Optional, TypeVar

from flask import current_app
from flask_sqlalchemy import BaseQuery
from sqlalchemy.orm import scoped_session
from werkzeug.exceptions import NotFound
from project.setup.db.models import Base
# -----------------------------------------------------------------------
T = TypeVar('T', bound=Base)
# -----------------------------------------------------------------------


class BaseDAO(Generic[T]):
    """The BaseDAO class provides base methods commonly using in the app"""
    __model__ = Base

    def __init__(self, db_session: scoped_session) -> None:
        """The initialization of the BaseDAO class

        :param db_session: a current session object
        """
        self._db_session = db_session

    @property
    def _items_per_page(self) -> int:
        """This method returns amount of items per page

        :return: the number of items per page
        """
        return current_app.config['ITEMS_PER_PAGE']

    def get_by_id(self, pk: int) -> Optional[T]:
        """This method returns a single item by id

        :param pk: the id of the item

        :return: a model representing the item
        """
        return self._db_session.query(self.__model__).get(pk)

    def get_all(self, page: Optional[int] = None) -> List[T]:
        """This method returns a list of items found in a certain table

        :param page: an optional parameter for page number to sort items by

        :return: a list of models representing the items
        """
        stmt: BaseQuery = self._db_session.query(self.__model__)
        if page:
            try:
                return stmt.paginate(page, self._items_per_page).items
            except NotFound:
                return []
        return stmt.all()

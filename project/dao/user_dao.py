"""The unit contains a UserDao class to work the 'genres' users"""
from project.dao.base import BaseDAO
from project.models import User
# ------------------------------------------------------------------------


class UserDao(BaseDAO[User]):
    """The UserDao class provides necessary methods to get data from the
    'users' table"""
    __model__ = User

    def get_by_email(self, email: str) -> User:
        """This method returns a user found by the provided email

        :param email: e-mail address of the searching user

        :returns: a User class model
        """
        user = self.__model__.query.filter(
            self.__model__.email == email).first()

        return user

    def add_new(self, d_user: dict) -> User:
        """This method adds a new user to the 'users' table

        :param d_user: a dictionary with a data to create a new record

        :returns:
        """
        new_user = self.__model__(**d_user)

        self._db_session.add(new_user)
        self._db_session.commit()

        return new_user

    def update(self, d_user: dict) -> None:
        """This method updates an existing user's data in the 'users' table

        :param d_user: a dictionary with a data to update
        """

        self._db_session.query(self.__model__).filter(
            self.__model__.email == d_user.get('email')).update(d_user)

        self._db_session.commit()

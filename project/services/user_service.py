"""The unit contains a UserService class with business logic to get data
from users table"""
from flask import abort
from project.services.base import BaseService
from project.dao import UserDao
# --------------------------------------------------------------------------


class UserService(BaseService[UserDao]):
    """The UserService clss provides a business logic to process user's
    requests regarding user table"""

    def update_data(self, d_user: dict) -> None:
        """This method serves to update the user data excepting a password

        :param d_user: a dictionary with user data to update
        """
        # if password in the d_user then we need to remove it
        if 'password' in d_user:
            del d_user['password']

        try:
            self.dao.update(d_user)

        except Exception as e:
            print(f'При обновлении данных возникла ошибка {e}')
            abort(400, 'Bad request')

    def update_password(self, d_user: dict) -> None:
        """This method serves to update the user's password

        :param d_user: a dictionary containing an old and new password
        """

        if 'password_2' in d_user:
            updated_data = {'email': d_user['email'],
                            'password': d_user['password_2']
                            }

            try:
                self.dao.update(updated_data)

            except Exception as e:
                print(f'При обновлении пароля возникла ошибка {e}')
                abort(400, 'Bad request')

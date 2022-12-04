"""The unit contains a AuthService class with business logic to authenticate
users, create tokens, hash passwords, etc."""
import datetime
import hashlib
import base64
from hmac import compare_digest
import jwt
import calendar
from flask import abort, current_app, request
from project.dao import UserDao
from project.models import User

from project.services.base import BaseService
# --------------------------------------------------------------------------


class AuthService(BaseService[UserDao]):
    """The AuthService class provides a business logic to authorize user's
    data, register new user and authorize users"""

    def register_user(self, d_user: dict) -> User:
        """The method registers a new user

        :param d_user: a dictionary with user's data

        :returns: the created model with user's data
        """

        if not d_user.get('email'):
            abort(400, 'Bad request')

        elif self.dao.get_by_email(d_user['email']):
            abort(400, 'User already exists')

        try:
            d_user['password'] = self._hash_password(d_user.get('password'))
            registered = self.dao.add_new(d_user)

            return registered

        except Exception as e:
            print(f'Не удалось добавить новую запись, возникла ошибка {e}')
            abort(400, 'Bad request')

    def authenticate_user(self, d_user: dict, refresh: bool = False) -> dict:
        """The method serves to authenticate user

        :param d_user: a dictionary with user's data
        :param refresh: a boolean indicating whether it is a log-in or a token
        refresh

        :returns: a dictionary with access and refresh tokens
        """
        user = self.dao.get_by_email(d_user.get('email'))

        if not user:
            abort(404, 'User not found')

        if not refresh:
            if not self._check_password(d_user.get('password'), user.password):

                abort(400, 'Wrong password')

        try:
            if 'password' in d_user:
                del d_user['password']

            tokens = self._create_tokens(d_user)

            return tokens

        except Exception as e:
            print(f'При создании токенов возникла ошибка {e}')
            abort(400)

    def update_tokens(self, d_tokens: dict) -> dict:
        """The method serves to update tokens

        :param d_tokens: a dictionary with access and refresh tokens

        :returns: a dictionary with new access and refresh tokens
        """
        refresh_token = d_tokens.get('refresh_token')

        user_data = self._decode_token(refresh_token)

        new_tokens = self.authenticate_user(user_data, refresh=True)

        return new_tokens

    def get_data_by_token(self, token: str) -> User:
        """This method returns a user model received by data getting from
        provided token

        :param token: a token to decode

        :returns: a model with requested data
        """
        token = self._fix_token(token)

        user_data = self._decode_token(token)

        full_data = self.dao.get_by_email(user_data.get('email'))

        if not full_data:
            abort(404, 'User not found')

        return full_data

    def auth_required(self, func):
        """This is a decorator to restrict access to the router for
        unauthenticated users

        :param func: the function to wrap

        :returns: wrapper-function
        """
        def wrapper(*args, **kwargs):
            """This function is a wrapper for func

            :param args: positional arguments
            :param kwargs: named arguments

            :returns: the wrapped function
            """
            access_token = request.headers.get('Authorization')

            if not access_token:
                abort(401, 'Authorization required')

            # removing 'Bearer' part of the token and decoding it
            access_token = self._fix_token(access_token)
            decoded_data = self._decode_token(access_token)

            # if user tries to work with users table then we need to check
            # if he has access to the certain user's data
            if 'user_id' in kwargs:

                found_user = self.dao.get_by_id(kwargs['user_id'])

                if not found_user:
                    abort(404, 'User not found')

                # if email received from token is not the same as received
                # from database then restrict access
                if found_user.email != decoded_data.get('email'):

                    abort(403, 'Access denied')

                if request.method == 'PUT':

                    user_data = request.json

                    # if user tries to change password then we need to check
                    # ald and new password and if both was provided
                    if not {'password_1', 'password_2'}.issubset(set(
                            user_data)):
                        abort(400, 'Bad request')

                    # hashing of a new password
                    user_data['password_2'] = self._hash_password(
                        user_data['password_2'])

                    # comparing provided password with one getting from
                    # a database
                    if not self._check_password(
                            user_data.get('password_1'), found_user.password):

                        abort(400, 'Wrong password')

            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def _fix_token(token: str):
        """This static method serves to get a token without additional
        information

        :param token: the token to be fixed

        :returns: the cleaned token
        """
        fixed_token = token.split('Bearer ')[-1]

        return fixed_token

    @staticmethod
    def _hash_password(password: str) -> bytes:
        """This static method serves to hash a password

        :param password: the password to be hashed

        :returns: the hashed base64-encoded password
        """
        if password:

            algo = current_app.config['PWD_ALGO']
            iterations = current_app.config['PWD_HASH_ITERATIONS']
            salt = current_app.config['PWD_HASH_SALT']

            hash_pass = hashlib.pbkdf2_hmac(algo, password.encode('utf-8'),
                                            salt, iterations)

            return base64.b64encode(hash_pass)

        raise Exception('Invalid data')

    def _check_password(self, provided_password: str, valid_password: str) ->\
            bool:
        """This method serves to validate a password

        :param provided_password: the password to be validated
        :param valid_password : the original password to compare with

        :returns: a boolean indicating if the password is valid
        """
        checked_password = self._hash_password(provided_password)

        return compare_digest(checked_password, valid_password)

    @staticmethod
    def _create_tokens(d_user: dict) -> dict:
        """This method serves to create tokens using provided user data

        :param d_user: the dictionary containing user's information

        :returns: a dictionary containing access and refresh tokens
        """
        algo = current_app.config['JWT_ALGO']
        secret = current_app.config['SECRET_KEY']

        access_expiration = datetime.datetime.utcnow() + \
        datetime.timedelta(minutes=current_app.config['TOKEN_EXPIRE_MINUTES'])

        d_user['exp'] = calendar.timegm(access_expiration.timetuple())

        access_token = jwt.encode(d_user, secret, algorithm=algo)

        refresh_expiration = datetime.datetime.utcnow() + \
                             datetime.timedelta(days=current_app.config[
                                 'TOKEN_EXPIRE_DAYS'])

        d_user['exp'] = calendar.timegm(refresh_expiration.timetuple())

        refresh_token = jwt.encode(d_user, secret, algorithm=algo)

        return {'access_token': access_token, 'refresh_token': refresh_token}

    @staticmethod
    def _decode_token(token: str) -> dict:
        """This method serves to decode a token

        :param token: the token to decode

        :returns: a decoded data
        """
        try:
            algo = current_app.config['JWT_ALGO']
            secret = current_app.config['SECRET_KEY']

            user_data = jwt.decode(token, secret, algorithms=[algo])

            return user_data

        except Exception as e:
            print(f'Не удалось декодировать токен, ошибка: {e}')
            abort(401)

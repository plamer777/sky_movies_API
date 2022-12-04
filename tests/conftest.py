"""This unit contains fixtures for testing purposes"""
import pytest
from project.config import TestingConfig
from project.server import create_app
from project.setup.db import db as database
# -------------------------------------------------------------------------


@pytest.fixture
def app():
    """This is a fixture representing an instance of Flask

    :return: a configured flask application
    """
    app = create_app(TestingConfig)
    with app.app_context():
        yield app


@pytest.fixture
def db(app):
    """This is a fixture creating a database and returning an instance of
    SQLAlchemy

    :param app: an instance of Flask

    :return: an instance of SQLAlchemy
    """
    database.init_app(app)
    database.drop_all()
    database.create_all()
    database.session.commit()

    yield database

    database.session.close()


@pytest.fixture
def client(app, db):
    """This is a fixture representing test client of the Flask application

    :param app: an instance of Flask
    :param db: an instance of SQLAlchemy

    :return: a test client of the Flask application
    """
    with app.test_client() as client:
        yield client


@pytest.fixture
def access_token():
    """This is a fixture representing test access token to test CBVs

    :return: a dictionary with access token
    """
    return {'Authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.'
                             'eyJlbWFpbCI6InBsYW1lcjg4QHlhbmRleC5ydSI'
                             'sInBhc3N3b3JkXzIiOiJjYWxpYnJhODgiLCJuYW1'
                             'lIjoiQWxla3NleSIsImV4cCI6MTY4MTI0NzQwNX0.'
                             '7KDx6Ifucp46gciwa_obaBvtUqFoadWzYw0Ey6TiMLE'}

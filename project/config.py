"""This unit contains configuration classes for testing, development and
production mode of application"""
import base64
import os
from pathlib import Path
from typing import Type
# -------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
# -------------------------------------------------------------------------


class BaseConfig:
    """The BaseConfig class contains common configuration fields"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'you-will-never-guess')
    JWT_ALGO = 'HS256'

    JSON_AS_ASCII = False

    ITEMS_PER_PAGE = 12

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    TOKEN_EXPIRE_MINUTES = 15
    TOKEN_EXPIRE_DAYS = 130

    PWD_ALGO = 'sha256'
    PWD_HASH_SALT = base64.b64decode("salt")
    PWD_HASH_ITERATIONS = 100_000

    RESTX_JSON = {
        'ensure_ascii': False,
    }


class TestingConfig(BaseConfig):
    """The TestingConfig class contains fields for testing purposes"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class DevelopmentConfig(BaseConfig):
    """The DevelopmentConfig class contains fields for development purposes"""
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + BASE_DIR.joinpath(
        'project.db').as_posix()


class ProductionConfig(BaseConfig):
    """The ProductionConfig class contains fields for production purposes"""
    DEBUG = False
    # TODO: дополнить конфиг


class ConfigFactory:
    """The ConfigFactory class serves to select configuration depending on
    FLASK_ENV environment variable"""
    flask_env = os.getenv('FLASK_ENV')

    @classmethod
    def get_config(cls) -> Type[BaseConfig]:
        if cls.flask_env == 'development':
            return DevelopmentConfig
        elif cls.flask_env == 'production':
            return ProductionConfig
        elif cls.flask_env == 'testing':
            return TestingConfig
        raise NotImplementedError


config = ConfigFactory.get_config()

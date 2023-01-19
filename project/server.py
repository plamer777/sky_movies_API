"""This unit contains functions to create a Flask application, configure it
and another objects like SQLAlchemy and Api instances"""
from flask import Flask, jsonify, render_template
from flask_cors import CORS
from project.exceptions import BaseServiceError
from project.setup.api import api
from project.setup.db import db
from project.views import auth_ns, genres_ns, user_ns, director_ns, movie_ns, \
    favorite_ns
# ------------------------------------------------------------------------


def base_service_error_handler(exception: BaseServiceError) -> tuple:
    return jsonify({'error': str(exception)}), exception.code


def create_app(config_obj) -> Flask:
    """This function creates a Flask application, configure SQLAlchemy and Api
    instances and register namespaces

    :param config_obj: configuration class

    :returns: created application
    """
    app = Flask(__name__)
    app.config.from_object(config_obj)

    @app.route('/')
    def index():
        return render_template('index.html')

    CORS(app=app)
    db.init_app(app)
    api.init_app(app)

    # Регистрация эндпоинтов
    api.add_namespace(auth_ns)
    api.add_namespace(user_ns)
    api.add_namespace(genres_ns)
    api.add_namespace(director_ns)
    api.add_namespace(movie_ns)
    api.add_namespace(favorite_ns)

    app.register_error_handler(BaseServiceError, base_service_error_handler)

    return app

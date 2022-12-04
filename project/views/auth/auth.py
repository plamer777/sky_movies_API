"""This unit contains a CBVs for routes like /auth/register/ and
/auth/login/"""
from flask import request
from flask_restx import Namespace, Resource
from project.container import auth_service
from project.setup.api.models import user
# ------------------------------------------------------------------------
auth_ns = Namespace('auth')
# --------------------------------- --------------------------------------


@auth_ns.route('/register/')
class RegisterView(Resource):
    """The RegisterView class is a CBV to process routes like
    /auth/register/"""
    @auth_ns.marshal_with(user, code=201, description='Created')
    def post(self):
        """This method processes POST requests

        :returns: JSON with created record
        """

        user_data = request.json

        return auth_service.register_user(user_data)


@auth_ns.route('/login/')
class LoginView(Resource):
    """The LoginView class is a CBV to process routes like
    /auth/login/"""

    def post(self):
        """This method processes POST requests

        :returns: JSON with an access and refresh token
        """
        user_data = request.json

        return auth_service.authenticate_user(user_data), 201

    def put(self):
        """This method processes PUT requests to refresh existing access
        token

        :returns: JSON with an access and refresh token
        """

        tokens = request.json

        return auth_service.update_tokens(tokens)

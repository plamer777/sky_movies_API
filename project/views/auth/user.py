"""This unit contains a CBVs for routes like /user/<user_id> and
/user/<user_id>/password/> """
from flask import request
from flask_restx import Namespace, Resource
from project.container import auth_service, user_service
from project.setup.api.models import user
# ------------------------------------------------------------------------
user_ns = Namespace('user')
# ------------------------------------------------------------------------


@user_ns.route('/<int:user_id>/')
class UserDataView(Resource):
    """The UserDataView class is a CBV to process routes like
    /user/<user_id>"""
    @user_ns.marshal_with(user, code=200, description='OK')
    @auth_service.auth_required
    def get(self, user_id: int):
        """This method processes GET requests

        :returns: JSON with user's data
        """

        return user_service.get_item(user_id)

    @auth_service.auth_required
    def patch(self, user_id: int):
        """This method processes PATCH requests to update user's data
        excepting a password

        :returns: a tuple with a result of the operation
        """

        user_data = request.json

        user_service.update_data(user_data)

        return 'Updated successfully', 204


@user_ns.route('/<int:user_id>/password/')
class UserPasswordView(Resource):
    """The UserDataView class is a CBV to process routes like
    /user/<user_id>/password"""

    @auth_service.auth_required
    def put(self, user_id: int):
        """This method processes PUT requests to update a password

        :returns: a tuple with a result of the operation
        """

        user_data = request.json

        user_service.update_password(user_data)

        return 'Updated successfully', 204

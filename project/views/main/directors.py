"""This unit contains a CBVs for routes like /directors/ and /directors/1"""
from flask_restx import Resource, Namespace
from project.setup.api.models import director
from project.setup.api.parsers import page_parser
from project.container import director_service, auth_service
# -----------------------------------------------------------------------
director_ns = Namespace('directors')
# -----------------------------------------------------------------------


@director_ns.route('/')
class DirectorsView(Resource):
    """The DirectorsView class is a CBV to process routes like /directors/"""
    @director_ns.expect(page_parser)
    @director_ns.marshal_with(director, as_list=True, description='OK',
                              code=200)
    @auth_service.auth_required
    def get(self):
        """This method processes GET requests

        :returns: JSON like a list of dictionaries with directors' data
        """
        return director_service.get_all(**page_parser.parse_args())


@director_ns.route('/<int:director_id>')
class DirectorView(Resource):
    """The DirectorView class is a CBV to process routes like /directors/1"""
    @director_ns.response(404, 'Not Found')
    @director_ns.marshal_with(director, description='OK', code=200)
    @auth_service.auth_required
    def get(self, director_id: int):
        """This method processes GET requests

        :param director_id: the id of the searching director

        :returns: JSON with director's data
        """
        return director_service.get_item(director_id)
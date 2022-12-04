"""This unit contains a CBVs for routes like /genres/ and /genres/1"""
from flask_restx import Namespace, Resource

from project.container import genre_service, auth_service
from project.setup.api.models import genre
from project.setup.api.parsers import page_parser
# ---------------------------------------------------------------------------
api = Namespace('genres')
# ---------------------------------------------------------------------------


@api.route('/')
class GenresView(Resource):
    """The GenresView class is a CBV to process routes like /genres/"""
    @api.expect(page_parser)
    @api.marshal_with(genre, as_list=True, code=200, description='OK')
    @auth_service.auth_required
    def get(self):
        """This method processes GET requests

        :returns: a JSON like a list of dictionaries with genres' data
        """
        return genre_service.get_all(**page_parser.parse_args())


@api.route('/<int:genre_id>/')
class GenreView(Resource):
    """The GenreView class is a CBV to process routes like /genres/1"""
    @api.response(404, 'Not Found')
    @api.marshal_with(genre, code=200, description='OK')
    @auth_service.auth_required
    def get(self, genre_id: int):
        """This method processes GET requests

        :param genre_id: the id of the searching genre

        :returns: JSON with genre's data
        """
        return genre_service.get_item(genre_id)

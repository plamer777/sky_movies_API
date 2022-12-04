"""This unit contains a CBVs for routes like /movies/ and /movies/1"""
from flask_restx import Namespace, Resource
from project.container import movie_service, auth_service
from project.setup.api.models import movie
from project.setup.api.parsers import movie_parser
# ---------------------------------------------------------------------------
movie_ns = Namespace('movies')
# ---------------------------------------------------------------------------


@movie_ns.route('/')
class MoviesView(Resource):
    """The MoviesView class is a CBV to process routes like /movies/"""
    @movie_ns.marshal_with(movie, code=200, description='OK', as_list=True)
    @movie_ns.expect(movie_parser)
    @auth_service.auth_required
    def get(self):
        """This method processes GET requests

        :returns: a JSON like a list of dictionaries with movies' data
        """

        return movie_service.get_all(**movie_parser.parse_args())


@movie_ns.route('/<int:movie_id>')
class MovieView(Resource):
    """The MovieView class is a CBV to process routes like /movies/1"""
    @movie_ns.response(404, 'Not Found')
    @movie_ns.marshal_with(movie, code=200, description='OK')
    @auth_service.auth_required
    def get(self, movie_id):
        """This method processes GET requests

        :param movie_id: the id of the searching movie

        :returns: JSON with movie's data
        """

        return movie_service.get_item(movie_id)

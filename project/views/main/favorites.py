from flask_restx import Resource, Namespace
from project.container import favorite_service, auth_service, user_service
from project.setup.api.models import user_movie
from project.setup.api.parsers import favorites_parser
# -------------------------------------------------------------------------
favorite_ns = Namespace('favorites/movies')
# -------------------------------------------------------------------------


@favorite_ns.route('/<int:movie_id>')
class FavoriteView(Resource):

    @favorite_ns.marshal_with(user_movie, code=201, description='Created')
    @favorite_ns.expect(favorites_parser)
    @auth_service.auth_required
    def post(self, movie_id: int):

        user = auth_service.get_data_by_token(
            *favorites_parser.parse_args().values())

        added, fav_genre_id = favorite_service.add({'user_id': user.id,
                                                    'movie_id': movie_id})
        user_service.update_data({'favorite_genre': fav_genre_id,
                                  'email': user.email})

        return added

    @favorite_ns.expect(favorites_parser)
    @auth_service.auth_required
    def delete(self, movie_id: int):

        user_id = auth_service.get_id_by_token(
            *favorites_parser.parse_args().values())

        favorite_service.remove({'user_id': user_id, 'movie_id': movie_id})

        return 'Deleted successfully', 204


@favorite_ns.route('/')
class FavoritesView(Resource):

    @favorite_ns.expect(favorites_parser)
    @favorite_ns.marshal_with(user_movie, code=201, description='OK',
                              as_list=True)
    @auth_service.auth_required
    def get(self):

        user_id = auth_service.get_id_by_token(
            *favorites_parser.parse_args().values())

        return favorite_service.get_by_user_id(user_id)

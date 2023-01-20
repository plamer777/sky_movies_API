"""The unit contains a flask_restx schemas to serialize SQLAlchemy models"""
from flask_restx import fields, Model
from project.setup.api import api
# ------------------------------------------------------------------------

# schema for genre models
genre: Model = api.model('Жанр', {
    'id': fields.Integer(required=True, example=1),
    'name': fields.String(required=True, max_length=100, example='Комедия'),
})

# schema for director models
director: Model = api.model('Директор', {
    'id': fields.Integer(required=True, example=1),
    'name': fields.String(required=True, example='James Cameron')
})

# schema for movie models
movie: Model = api.model('Фильм', {
    'id': fields.Integer(required=True, example=1),
    'title': fields.String(required=True, example='Назад в будущее'),
    'description': fields.String(required=True, example='Док и Марти '
                                                        'отправляются...'),
    'trailer': fields.String(required=True, example='https://youtube.com'),
    'year': fields.Integer(required=True, example=1984),
    'rating': fields.Float(required=True, example=10.0),
    'genre_id': fields.Integer(required=True, example=3),
    'director_id': fields.Integer(required=True, example=5)
})

# schema for user models
user: Model = api.model('Пользователь', {
    'id': fields.Integer(required=True, example=1),
    'email': fields.String(required=True, example='plamer88@yandex.ru'),
    'name': fields.String(required=True, example='Вася'),
    'surname': fields.String(required=True, example='Пупкин'),
    'favorite_genre': fields.String(required=True, example='Ужасы')
})

# schema for user_movie models
user_movie: Model = api.model('Избранные', {
    'id': fields.Integer(required=True, example=1),
    'user_id': fields.Integer(required=True, example=1),
    'movie_id': fields.Integer(required=True, example=1)
})

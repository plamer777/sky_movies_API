from .genres import api as genres_ns
from .directors import director_ns
from .movies import movie_ns
from .favorites import favorite_ns

__all__ = [
    'genres_ns',
    'director_ns',
    'movie_ns',
    'favorite_ns'
]

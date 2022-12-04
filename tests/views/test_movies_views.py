"""This unit contains the TestMoviesView to test CBVs for /movies/ 
route"""
import pytest
from project.models import Movie
# ------------------------------------------------------------------------


class TestMoviesView:
    """The TestMoviesView provides all necessary methods to test CBVs for
    /movies/ route"""

    @pytest.fixture
    def movie(self, db):
        """This method is a fixture returning a Movie instance

        :param db: the fixture representing the SQLAlchemy instance

        :return: a Movie instance
        """
        obj = Movie(
            title='Best movie',
            description='test description',
            trailer='https://test',
            year=2005,
            rating=8.3,
            genre_id=5,
            director_id=2
        )
        db.session.add(obj)
        db.session.commit()
        return obj

    def test_many(self, client, movie, access_token):
        """This method serves to test /movies/ route

        :param client: the test client
        :param movie: an instance of Movie class
        :param access_token: the access token to get access to the CBV
        """
        response = client.get("/movies/", headers=access_token)
        assert response.status_code == 200
        assert response.json == [{"id": movie.id, "title": movie.title,
                                  'description': movie.description,
                                  'trailer': movie.trailer,
                                  'year': movie.year,
                                  'rating': movie.rating,
                                  'genre_id': movie.genre_id,
                                  'director_id': movie.director_id}]

    def test_movie_pages(self, client, movie, access_token):
        """This method serves to test /movies/?page=1 route

        :param client: the test client
        :param movie: an instance of Movie class
        :param access_token: the access token to get access to the CBV
        """
        response = client.get("/movies/?page=1", headers=access_token)
        assert response.status_code == 200
        assert len(response.json) == 1

        response = client.get("/movies/?page=2", headers=access_token)
        assert response.status_code == 200
        assert len(response.json) == 0

    def test_movie(self, client, movie, access_token):
        """This method serves to test /movies/1 route

        :param client: the test client
        :param movie: an instance of Movie class
        :param access_token: the access token to get access to the CBV
        """

        response = client.get("/movies/1", headers=access_token)
        assert response.status_code == 200
        assert response.json == {"id": movie.id, "title": movie.title,
                                 'description': movie.description,
                                 'trailer': movie.trailer,
                                 'year': movie.year,
                                 'rating': movie.rating,
                                 'genre_id': movie.genre_id,
                                 'director_id': movie.director_id}

    def test_movie_not_found(self, client, movie, access_token):
        """This method serves to test /movies/2 route

        :param client: the test client
        :param movie: an instance of Movie class
        :param access_token: the access token to get access to the CBV
        """
        response = client.get("/movies/2", headers=access_token)
        assert response.status_code == 404

"""This unit contains TestMoviesDAO class to test MovieDAO"""
import pytest
from project.dao import MovieDao
from project.models import Movie
# --------------------------------------------------------------------------


class TestMoviesDAO:
    """The TestMoviesDAO class provides methods to test the MovieDAO
    class"""
    @pytest.fixture
    def movies_dao(self, db):
        """This is a fixture returning a MovieDAO instance

        :param db: the fixture representing the SQLAlchemy instance

        :return: a MovieDAO instance
        """
        return MovieDao(db.session)

    @pytest.fixture
    def movie_1(self, db):
        """This is a fixture returning a Movie instance

        :param db: the fixture representing the SQLAlchemy instance

        :return: a Movie instance
        """
        movie = Movie(
            title='Best movie_1',
            description='test description',
            trailer='https://test',
            year=2005,
            rating=8.3,
            genre_id=5,
            director_id=2
        )
        db.session.add(movie)
        db.session.commit()
        return movie

    @pytest.fixture
    def movie_2(self, db):
        """This is a fixture returning a Movie instance

        :param db: the fixture representing the SQLAlchemy instance

        :return: a Movie instance
        """
        movie = Movie(
            title='Best movie_2',
            description='test description1',
            trailer='https://test1',
            year=2008,
            rating=6.3,
            genre_id=2,
            director_id=5
        )
        db.session.add(movie)
        db.session.commit()
        return movie

    def test_get_movie_by_id(self, movie_1, movies_dao):
        """This method tests the get_by_id method of a MovieDAO

        :param movie_1: a fixture returning Movie instance
        :param movies_dao: a MovieDAO instance
        """
        assert movies_dao.get_by_id(movie_1.id) == movie_1

    def test_get_movie_by_id_not_found(self, movies_dao):
        """This method tests the get_by_id method of a MovieDAO when record
        was not found

        :param movies_dao: a MovieDAO instance
        """
        assert not movies_dao.get_by_id(1)

    def test_get_all_movies(self, movies_dao, movie_1, movie_2):
        """This method tests the get_all method of a MovieDAO

        :param movie_1: a fixture returning Movie instance
        :param movie_2: a fixture returning Movie instance
        :param movies_dao: a MovieDAO instance
        """
        assert movies_dao.get_all() == [movie_1, movie_2]

    def test_get_movies_by_page(self, app, movies_dao, movie_1,
                                movie_2):
        """This method tests the get_all method of a MovieDAO

        :param app: the fixture representing the Flask instance
        :param movie_1: a fixture returning Movie instance
        :param movie_2: a fixture returning Movie instance
        :param movies_dao: a MovieDAO instance
        """
        app.config['ITEMS_PER_PAGE'] = 1
        assert movies_dao.get_all(page=1) == [movie_1]
        assert movies_dao.get_all(page=2) == [movie_2]
        assert movies_dao.get_all(page=3) == []

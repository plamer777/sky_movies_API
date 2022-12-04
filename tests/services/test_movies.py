"""This unit contains a TestMoviesService to test the MovieService class"""
from unittest.mock import patch
import pytest
from project.exceptions import ItemNotFound
from project.models import Movie
from project.services import MovieService
# --------------------------------------------------------------------------


class TestMoviesService:
    """The TestMoviesService provides all methods to test the MovieService"""
    @pytest.fixture()
    @patch('project.dao.MovieDao')
    def movies_dao_mock(self, dao_mock):
        """This method is a fixture representing a mocked MovieDAO instance

        :param dao_mock: A mocked MovieDAO class

        :returns: A mocked MovieDAO instance returning certain data
        """
        dao = dao_mock()
        dao.get_by_id.return_value = Movie(
            title='Best movie',
            description='test description',
            trailer='https://test',
            year=2005,
            rating=8.3,
            genre_id=5,
            director_id=2
        )
        dao.get_all.return_value = [
            Movie(
                title='Best movie_1',
                description='test description',
                trailer='https://test',
                year=2005,
                rating=8.3,
                genre_id=5,
                director_id=2
            ),
            Movie(
                title='Best movie_2',
                description='test description_2',
                trailer='https://test_2',
                year=2007,
                rating=7.3,
                genre_id=2,
                director_id=5
            ),
        ]
        return dao

    @pytest.fixture()
    def movies_service(self, movies_dao_mock):
        """This method is a fixture representing a MovieService instance

        :param movies_dao_mock: A mocked MovieDAO instance

        :returns: MovieService instance
        """
        return MovieService(dao=movies_dao_mock)

    @pytest.fixture
    def movie(self, db):
        """This method is a fixture representing an instance of a Movie
        class

        :param db: a fixture representing SQLAlchemy instance
        """
        obj = Movie(
            title='movie',
            description='description',
            trailer='https://test',
            year=2005,
            rating=8.3,
            genre_id=5,
            director_id=2
        )
        db.session.add(obj)
        db.session.commit()
        return obj

    def test_get_movie(self, movies_service, movie):
        """This method serves to test the MovieService's method - get_item

        :param movies_service: an instance of a MovieService
        :param movie: an instance of a Movie class
        """
        assert movies_service.get_item(movie.id)

    def test_movie_not_found(self, movies_dao_mock, movies_service):
        """This method serves to test the MovieService's method get_item if
        item's id is wrong

        :param movies_dao_mock: a mocked MovieDAO instance
        :param movies_service: an instance of the MovieService class
        """
        movies_dao_mock.get_by_id.return_value = None

        with pytest.raises(ItemNotFound):
            movies_service.get_item(10)

    @pytest.mark.parametrize('page', [1, None], ids=['with page',
                                                     'without page'])
    def test_get_movies(self, movies_dao_mock, movies_service, page):
        """This method serves to test the MovieService's method get_all

        :param movies_dao_mock: a mocked MovieDAO instance
        :param movies_service: an instance of the MovieService class
        :param page: the page number to test
        """
        movies = movies_service.get_all(page=page, status=None)
        assert len(movies) == 2
        assert movies == movies_dao_mock.get_all.return_value
        movies_dao_mock.get_all.assert_called_with(page=page, status=None)

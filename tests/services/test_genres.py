"""This unit contains a TestGenresService to test the GenreService class"""
from unittest.mock import patch
import pytest
from project.exceptions import ItemNotFound
from project.models import Genre
from project.services import GenreService
# --------------------------------------------------------------------------


class TestGenresService:
    """The TestGenresService provides all methods to test the GenreService"""
    @pytest.fixture()
    @patch('project.dao.GenresDAO')
    def genres_dao_mock(self, dao_mock):
        """This method is a fixture representing a mocked GenreDAO instance

        :param dao_mock: A mocked GenreDAO class

        :returns: A mocked GenreDAO instance returning certain data
        """
        dao = dao_mock()
        dao.get_by_id.return_value = Genre(id=1, name='test_genre')
        dao.get_all.return_value = [
            Genre(id=1, name='test_genre_1'),
            Genre(id=2, name='test_genre_2'),
        ]
        return dao

    @pytest.fixture()
    def genres_service(self, genres_dao_mock):
        """This method is a fixture representing a GenreService instance

        :param genre_dao_mock: A mocked GenreDAO instance

        :returns: GenreService instance
        """
        return GenreService(dao=genres_dao_mock)

    @pytest.fixture
    def genre(self, db):
        """This method is a fixture representing an instance of a Genre
        class

        :param db: a fixture representing SQLAlchemy instance
        """
        obj = Genre(name="genre")
        db.session.add(obj)
        db.session.commit()
        return obj

    def test_get_genre(self, genres_service, genre):
        """This method serves to test the GenreService's method - get_item

        :param genres_service: an instance of a GenreService
        :param genre: an instance of a Genre class
        """
        assert genres_service.get_item(genre.id)

    def test_genre_not_found(self, genres_dao_mock, genres_service):
        """This method serves to test the GenreService's method get_item if
        item's id is wrong

        :param genres_dao_mock: a mocked GenreDAO instance
        :param genres_service: an instance of the GenreService class
        """
        genres_dao_mock.get_by_id.return_value = None

        with pytest.raises(ItemNotFound):
            genres_service.get_item(10)

    @pytest.mark.parametrize('page', [1, None], ids=['with page',
                                                     'without page'])
    def test_get_genres(self, genres_dao_mock, genres_service, page):
        """This method serves to test the GenreService's method get_all

        :param genres_dao_mock: a mocked GenreDAO instance
        :param genres_service: an instance of the GenreService class
        :param page: the page number to test
        """
        genres = genres_service.get_all(page=page)
        assert len(genres) == 2
        assert genres == genres_dao_mock.get_all.return_value
        genres_dao_mock.get_all.assert_called_with(page=page)

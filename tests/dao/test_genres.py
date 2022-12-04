"""This unit contains TestGenresDAO class to test GenresDAO"""
import pytest
from project.dao import GenresDAO
from project.models import Genre
# --------------------------------------------------------------------------


class TestGenresDAO:
    """The TestGenresDAO class provides methods to test the GenreDAO class"""
    @pytest.fixture
    def genres_dao(self, db):
        """This is a fixture returning a GenreDAO instance

        :param db: the fixture representing the SQLAlchemy instance

        :return: a GenreDAO instance
        """
        return GenresDAO(db.session)

    @pytest.fixture
    def genre_1(self, db):
        """This is a fixture returning a Genre instance

        :param db: the fixture representing the SQLAlchemy instance

        :return: a Genre instance
        """
        g = Genre(name="Боевик")
        db.session.add(g)
        db.session.commit()
        return g

    @pytest.fixture
    def genre_2(self, db):
        """This is a fixture returning a Genre instance

        :param db: the fixture representing the SQLAlchemy instance

        :return: a Genre instance
        """
        g = Genre(name="Комедия")
        db.session.add(g)
        db.session.commit()
        return g

    def test_get_genre_by_id(self, genre_1, genres_dao):
        """This method tests the get_by_id method of a GenreDAO

        :param genre_1: a fixture returning Genre instance
        :param genres_dao: a GenreDAO instance
        """
        assert genres_dao.get_by_id(genre_1.id) == genre_1

    def test_get_genre_by_id_not_found(self, genres_dao):
        """This method tests the get_by_id method of a GenreDAO when record
        was not found

        :param genres_dao: a GenreDAO instance
        """
        assert not genres_dao.get_by_id(1)

    def test_get_all_genres(self, genres_dao, genre_1, genre_2):
        """This method tests the get_all method of a GenreDAO

        :param genre_1: a fixture returning Genre instance
        :param genre_2: a fixture returning Genre instance
        :param genres_dao: a GenreDAO instance
        """
        assert genres_dao.get_all() == [genre_1, genre_2]

    def test_get_genres_by_page(self, app, genres_dao, genre_1, genre_2):
        """This method tests the get_all method of a GenreDAO

        :param app: the fixture representing the Flask instance
        :param genre_1: a fixture returning Genre instance
        :param genre_2: a fixture returning Genre instance
        :param genres_dao: a GenreDAO instance
        """
        app.config['ITEMS_PER_PAGE'] = 1
        assert genres_dao.get_all(page=1) == [genre_1]
        assert genres_dao.get_all(page=2) == [genre_2]
        assert genres_dao.get_all(page=3) == []

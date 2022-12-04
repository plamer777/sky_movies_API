"""This unit contains TestDirectorsDAO class to test DirectorDAO"""
import pytest
from project.dao import DirectorDao
from project.models import Director
# --------------------------------------------------------------------------


class TestDirectorsDAO:
    """The TestDirectorsDAO class provides methods to test the DirectorDAO
    class"""
    @pytest.fixture
    def directors_dao(self, db):
        """This is a fixture returning a DirectorDAO instance

        :param db: the fixture representing the SQLAlchemy instance

        :return: a DirectorDAO instance
        """
        return DirectorDao(db.session)

    @pytest.fixture
    def director_1(self, db):
        """This is a fixture returning a Director instance

        :param db: the fixture representing the SQLAlchemy instance

        :return: a Director instance
        """
        director = Director(name="Люк Бессон")
        db.session.add(director)
        db.session.commit()
        return director

    @pytest.fixture
    def director_2(self, db):
        """This is a fixture returning a Director instance

        :param db: the fixture representing the SQLAlchemy instance

        :return: a Director instance
        """
        director = Director(name="Джеймс Камерон")
        db.session.add(director)
        db.session.commit()
        return director

    def test_get_director_by_id(self, director_1, directors_dao):
        """This method tests the get_by_id method of a DirectorDAO

        :param director_1: a fixture returning Director instance
        :param directors_dao: a DirectorDAO instance
        """
        assert directors_dao.get_by_id(director_1.id) == director_1

    def test_get_director_by_id_not_found(self, directors_dao):
        """This method tests the get_by_id method of a DirectorDAO when record
        was not found

        :param directors_dao: a DirectorDAO instance
        """
        assert not directors_dao.get_by_id(1)

    def test_get_all_directors(self, directors_dao, director_1, director_2):
        """This method tests the get_all method of a DirectorDAO

        :param director_1: a fixture returning Director instance
        :param director_2: a fixture returning Director instance
        :param directors_dao: a DirectorDAO instance
        """
        assert directors_dao.get_all() == [director_1, director_2]

    def test_get_directors_by_page(self, app, directors_dao, director_1,
                                   director_2):
        """This method tests the get_all method of a DirectorDAO

        :param app: the fixture representing the Flask instance
        :param director_1: a fixture returning Director instance
        :param director_2: a fixture returning Director instance
        :param directors_dao: a DirectorDAO instance
        """
        app.config['ITEMS_PER_PAGE'] = 1
        assert directors_dao.get_all(page=1) == [director_1]
        assert directors_dao.get_all(page=2) == [director_2]
        assert directors_dao.get_all(page=3) == []

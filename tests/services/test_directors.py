"""This unit contains a TestDirectorsService to test the DirectorService
class"""
from unittest.mock import patch
import pytest
from project.exceptions import ItemNotFound
from project.models import Director
from project.services import DirectorService
# --------------------------------------------------------------------------


class TestDirectorsService:
    """The TestDirectorsService provides all methods to test the
    DirectorService"""
    @pytest.fixture()
    @patch('project.dao.DirectorDao')
    def directors_dao_mock(self, dao_mock):
        """This method is a fixture representing a mocked DirectorDAO instance

        :param dao_mock: A mocked DirectorDAO class

        :returns: A mocked DirectorDAO instance returning certain data
        """
        dao = dao_mock()
        dao.get_by_id.return_value = Director(id=1, name='test_director')
        dao.get_all.return_value = [
            Director(id=1, name='test_director_1'),
            Director(id=2, name='test_director_2'),
        ]
        return dao

    @pytest.fixture()
    def directors_service(self, directors_dao_mock):
        """This method is a fixture representing a DirectorService instance

        :param directors_dao_mock: A mocked DirectorDAO instance

        :returns: DirectorService instance
        """
        return DirectorService(dao=directors_dao_mock)

    @pytest.fixture
    def director(self, db):
        """This method is a fixture representing an instance of a Director
        class

        :param db: a fixture representing SQLAlchemy instance
        """
        obj = Director(name="director")
        db.session.add(obj)
        db.session.commit()
        return obj

    def test_get_director(self, directors_service, director):
        """This method serves to test the DirectorService's method - get_item

        :param directors_service: an instance of a DirectorService
        :param director: an instance of a Director class
        """
        assert directors_service.get_item(director.id)

    def test_director_not_found(self, directors_dao_mock, directors_service):
        """This method serves to test the DirectorService's method get_item if
        item's id is wrong

        :param directors_dao_mock: a mocked DirectorDAO instance
        :param directors_service: an instance of the DirectorService class
        """
        directors_dao_mock.get_by_id.return_value = None

        with pytest.raises(ItemNotFound):
            directors_service.get_item(10)

    @pytest.mark.parametrize('page', [1, None],
                             ids=['with page', 'without page'])
    def test_get_directors(self, directors_dao_mock, directors_service, page):
        """This method serves to test the DirectorService's method get_all

        :param directors_dao_mock: a mocked DirectorDAO instance
        :param directors_service: an instance of the DirectorService class
        :param page: the page number to test
        """
        directors = directors_service.get_all(page=page)
        assert len(directors) == 2
        assert directors == directors_dao_mock.get_all.return_value
        directors_dao_mock.get_all.assert_called_with(page=page)

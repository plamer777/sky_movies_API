"""This unit contains the TestDirectorsView to test CBVs for /directors/
 route"""
import pytest
from project.models import Director
# ------------------------------------------------------------------------


class TestDirectorsView:
    """The TestDirectorsView provides all necessary methods to test CBVs for
    /directors/ route"""

    @pytest.fixture
    def director(self, db):
        """This method is a fixture returning a Director instance

        :param db: the fixture representing the SQLAlchemy instance

        :return: a Director instance
        """
        obj = Director(name="director_1")
        db.session.add(obj)
        db.session.commit()
        return obj

    def test_many(self, client, director, access_token):
        """This method serves to test /directors/ route

        :param client: the test client
        :param director: an instance of Director class
        :param access_token: the access token to get access to the CBV
        """
        response = client.get("/directors/", headers=access_token)
        assert response.status_code == 200
        assert response.json == [{"id": director.id, "name": director.name}]

    def test_director_pages(self, client, director, access_token):
        """This method serves to test /directors/?page=1 route

        :param client: the test client
        :param director: an instance of Director class
        :param access_token: the access token to get access to the CBV
        """
        response = client.get("/directors/?page=1", headers=access_token)
        assert response.status_code == 200
        assert len(response.json) == 1

        response = client.get("/directors/?page=2", headers=access_token)
        assert response.status_code == 200
        assert len(response.json) == 0

    def test_director(self, client, director, access_token):
        """This method serves to test /directors/1 route

        :param client: the test client
        :param director: an instance of Director class
        :param access_token: the access token to get access to the CBV
        """

        response = client.get("/directors/1", headers=access_token)
        assert response.status_code == 200
        assert response.json == {"id": director.id, "name": director.name}

    def test_director_not_found(self, client, director, access_token):
        """This method serves to test /directors/2 route

        :param client: the test client
        :param director: an instance of Director class
        :param access_token: the access token to get access to the CBV
        """
        response = client.get("/directors/2", headers=access_token)
        assert response.status_code == 404

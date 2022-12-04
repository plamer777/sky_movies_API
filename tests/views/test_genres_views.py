"""This unit contains the TestGenresView to test CBVs for /genres/ route"""
import pytest
from project.models import Genre
# ------------------------------------------------------------------------


class TestGenresView:
    """The TestGenresView provides all necessary methods to test CBVs for
    /genres/ route"""
    @pytest.fixture
    def genre(self, db):
        """This method is a fixture returning a Genre instance

        :param db: the fixture representing the SQLAlchemy instance

        :return: a Director instance
        """
        obj = Genre(name="genre")
        db.session.add(obj)
        db.session.commit()
        return obj

    def test_many(self, client, genre, access_token):
        """This method serves to test /genres/ route

        :param client: the test client
        :param genre: an instance of Genre class
        :param access_token: the access token to get access to the CBV
        """
        response = client.get("/genres/", headers=access_token)
        assert response.status_code == 200
        assert response.json == [{"id": genre.id, "name": genre.name}]

    def test_genre_pages(self, client, genre, access_token):
        """This method serves to test /genres/?page=1 route

        :param client: the test client
        :param genre: an instance of Genre class
        :param access_token: the access token to get access to the CBV
        """
        response = client.get("/genres/?page=1", headers=access_token)
        assert response.status_code == 200
        assert len(response.json) == 1

        response = client.get("/genres/?page=2", headers=access_token)
        assert response.status_code == 200
        assert len(response.json) == 0

    def test_genre(self, client, genre, access_token):
        """This method serves to test /genres/1 route

        :param client: the test client
        :param genre: an instance of Genre class
        :param access_token: the access token to get access to the CBV
        """

        response = client.get("/genres/1/", headers=access_token)
        assert response.status_code == 200
        assert response.json == {"id": genre.id, "name": genre.name}

    def test_genre_not_found(self, client, genre, access_token):
        """This method serves to test /genres/2 route

        :param client: the test client
        :param genre: an instance of Genre class
        :param access_token: the access token to get access to the CBV
        """
        response = client.get("/genres/2/", headers=access_token)
        assert response.status_code == 404

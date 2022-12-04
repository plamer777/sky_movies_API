"""The unit contains a DirectorService class with business logic for directors
table of the database"""
from project.services.base import BaseService
from project.dao import DirectorDao
# --------------------------------------------------------------------------


class DirectorService(BaseService[DirectorDao]):
    """The DirectorService class provides a business logic to work with
    directors table"""
    pass

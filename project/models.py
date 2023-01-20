"""The unit contains classes serving to create a database models and to
serialize and deserialize the models"""
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from marshmallow import Schema, fields
from sqlalchemy.orm import relationship
from project.setup.db import models
# -------------------------------------------------------------------------


class Genre(models.Base):
    """The Genre class represents a model to work with the genres table"""
    __tablename__ = 'genres'

    name = Column(String(100), unique=True, nullable=False)


class GenreSchema(Schema):
    """The GenreSchema class serves to serialize and deserialize genre
    models"""
    id = fields.Int()
    name = fields.Str()


class Director(models.Base):
    """The Director class represents a model to work with the directors
    table"""
    __tablename__ = 'directors'
    name = Column(String(30), unique=True, nullable=False)


class DirectorSchema(Schema):
    """The DirectorSchema class serves to serialize and deserialize director
        models"""
    id = fields.Int()
    name = fields.Str()


class Movie(models.Base):
    """The Movie class represents a model to work with the movies table"""
    __tablename__ = 'movies'

    title = Column(String(50), nullable=False)
    description = Column(String(100), nullable=False)
    trailer = Column(String(100), nullable=False)
    year = Column(Integer(), nullable=False)
    rating = Column(Float(), nullable=False)
    genre_id = Column(Integer(), ForeignKey('genres.id'), nullable=False)
    director_id = Column(Integer(), ForeignKey('directors.id'), nullable=False)
    genre = relationship('Genre', backref='movies')
    director = relationship('Director', backref='movies')


class MovieSchema(Schema):
    """The MovieSchema class serves to serialize and deserialize movie
    models"""
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre_id = fields.Int()
    director_id = fields.Int()


class User(models.Base):
    """The User class represents a model to work with the users table"""
    __tablename__ = 'users'

    email = Column(String(30), nullable=False)
    password = Column(String(30), nullable=False)
    name = Column(String(20))
    surname = Column(String(20))
    favorite_genre = Column(Integer(), ForeignKey('genres.id'))
    best_genre = relationship('Genre')


class UserSchema(Schema):
    """The UserSchema class serves to serialize and deserialize user
    models"""
    id = fields.Int()
    email = fields.Str()
    password = fields.Str()
    name = fields.Str()
    surname = fields.Str()
    favorite_genre = fields.Str()


class UserMovie(models.Base):
    """The UserMovie class represents a model to work with the users_movies
    table"""
    __tablename__ = 'users_movies'

    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    movie_id = Column(Integer, ForeignKey('movies.id'), nullable=True)
    user = relationship('User')
    movie = relationship('Movie')

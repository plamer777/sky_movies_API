"""This unit contains a logic to create an empty database"""
from project.config import config
from project.server import create_app
from project.setup.db import db
# -------------------------------------------------------------------------

if __name__ == '__main__':
    with create_app(config).app_context():
        db.create_all()

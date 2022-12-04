"""This is a main file to run an application"""
from project.config import config
from project.models import Genre, Director
from project.server import create_app, db
# -------------------------------------------------------------------------
app = create_app(config)
# -------------------------------------------------------------------------


@app.shell_context_processor
def shell():
    return {
        "db": db,
        "Genre": Genre,
        "Director": Director
    }

from flask import Flask
from pasteapp.views.frontend import frontend
from pasteapp.database import initialise_engine

def create_app(cfg_file):
    app = Flask(__name__)
    app.config.from_pyfile(cfg_file)

    db_uri = app.config['DATABASE']
    initialise_engine(db_uri)

    app.register_blueprint(frontend)
    return app

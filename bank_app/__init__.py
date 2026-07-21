from pathlib import Path

from flask import Flask

from .bootstrap import seed_data
from .blueprints import ALL_BLUEPRINTS
from .context import register_context_processors
from .extensions import db
from .filters import register_jinja_filters
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    Path(app.config["UPLOAD_FOLDER"]).mkdir(parents=True, exist_ok=True)
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    db.init_app(app)
    register_jinja_filters(app)

    for blueprint in ALL_BLUEPRINTS:
        app.register_blueprint(blueprint)

    register_context_processors(app)
    seed_data(app)
    return app

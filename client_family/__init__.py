from flask import Flask, redirect, url_for
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
from .app import init_admin, init_db, init_migrate, init_blueprints
from .models import db 
from .logger import logging

load_dotenv()

logger = logging.getLogger(__package__)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.urandom(12).hex()
    init_db(app)
    init_migrate(app)
    init_admin(app)
    init_blueprints(app)

    # Re routes root of flask admin
    app.add_url_rule('/', 'index', lambda: redirect(url_for("client_family.index_view")))

    match os.getenv('ENV', 'dev').lower():
        case 'dev':
            app.debug = True
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
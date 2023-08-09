from flask import Flask
from flask_migrate import Migrate
from .models import db

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://nbastida@localhost:5432/sqladmin'
    db.init_app(app)
    migrate = Migrate(app, db)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
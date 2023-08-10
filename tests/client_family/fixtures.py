import pytest
import subprocess
from client_family.models import db
from client_family import create_app as create_app_import

@pytest.fixture(scope='module')
def test_database():
    # Create a new test database
    subprocess.run(['createdb', 'test_db'])
    
    # Copy the schema from the production database
    subprocess.run(['pg_dump', '--schema-only', 'sqladmin', '|', 'psql', 'test_db'])
    
    # Set up the SQLAlchemy connection
    db.engine.url.database = 'test_db'
    db.create_all()
    
    yield db

    # Drop the test database
    subprocess.run(['dropdb', 'test_db'])

@pytest.fixture(scope='module')
def test_app():
    app = create_app_import()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/test_db'
    app.config['TESTING'] = True
    return app


@pytest.fixture(scope='function')
def test_client(test_database, test_app):
    with test_app.app_context():
        db.drop_all()
        db.create_all()

        yield test_app.test_client()
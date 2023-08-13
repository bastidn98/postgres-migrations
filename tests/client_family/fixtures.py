import pytest
import subprocess
import os
from client_family.models import db
from client_family import create_app as create_app_import

@pytest.fixture(scope='module')
def test_app():
    os.environ['ENV'] = 'test' # Sets app to use dockerised testdb (which is a duplicate of prod)
    app = create_app_import()
    app.config['TESTING'] = True
    return app

@pytest.fixture(scope='function')
def test_client(test_database, test_app):
    with test_app.app_context():
        db.drop_all()
        db.create_all()

        yield test_app.test_client()
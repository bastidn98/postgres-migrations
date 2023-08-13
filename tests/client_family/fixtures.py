import pytest
import subprocess
import os
from client_family.models import db
from client_family import create_app as create_app_import

@pytest.fixture(scope='module')
def test_app():
    os.environ['ENV'] = 'test' # Sets app to use dockerized testdb (which is a duplicate of prod)
    app = create_app_import()
    app.config['TESTING'] = True
    return app

@pytest.fixture(scope='function')
def test_client(test_app): # Pass test_app as an argument here
    with test_app.app_context():
        client = test_app.test_client()
        yield client
        meta = db.metadata
        db.session.rollback()
        for table in reversed(meta.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()
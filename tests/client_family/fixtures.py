import pytest
import subprocess
import os
from client_family.models import db
from client_family import create_app as create_app_import

@pytest.fixture(scope='function')
def test_app():
    os.environ['DEV_DBNAME'] = 'test'
    os.environ['REBUILD_DB'] = 'true'
    app = create_app_import()
    app.config['TESTING'] = True
    with app.app_context():
        yield app
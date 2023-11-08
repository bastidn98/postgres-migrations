import pytest
from .fixtures import test_app, runner
from client_family.models import db, ClientFamily
from client_family.importer import import_data_from_excel

@pytest.mark.ext_files
def test_import_data_from_excel(test_app, runner):
    '''Note, needs a test excel file'''
    prev_len = len(ClientFamily.query.all())
    result = runner.invoke(import_data_from_excel, args=['~/Code/sqladmin/excel_test.xlsx', 'Client'])
    assert result.exit_code == 0
    assert len(ClientFamily.query.all()) > prev_len 
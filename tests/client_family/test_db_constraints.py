import pytest
from .fixtures import test_client
from client_family.models import db, ClientFamily

def test_family_head_exists_as_client(test_client):
    existing_client = ClientFamily(client='client1', family_head='family_head1')
    db.session.add(existing_client)
    db.session.commit()

    with pytest.raises(Exception):
        new_client_family = ClientFamily(client='client2', family_head='client1')
        db.session.add(new_client_family)
        db.session.commit()

def test_client_exists_as_family_head(test_client):
    existing_client = ClientFamily(client='client1', family_head='family_head1')
    db.session.add(existing_client)
    db.session.commit()

    with pytest.raises(Exception):
        new_client_family = ClientFamily(client='family_head1', family_head='family_head2')
        db.session.add(new_client_family)
        db.session.commit()

def test_add_client_family_successfully(test_client):
    new_client_family = ClientFamily(client='client1', family_head='family_head1')
    db.session.add(new_client_family)
    db.session.commit()

    client_family = ClientFamily.query.first()
    assert client_family.client == 'client1'
    assert client_family.family_head == 'family_head1'


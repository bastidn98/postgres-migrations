from flask_sqlalchemy import SQLAlchemy
import boto3
from sqlalchemy import event, DDL
from sqlalchemy.schema import CheckConstraint
import os

db = SQLAlchemy()

class ClientFamily(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client = db.Column(db.String(), nullable=False, unique=True)
    family_head = db.Column(db.String(), nullable=False)
    
    __table_args__= (
        CheckConstraint(client!=family_head, name='check_client_head_entry_constraint'),
    )

    # NOTE: There is a database trigger associated with this table that enforces
    # additional constraints. The constraint makes it soa new ClientFamily cant 
    # have a family_head that already exists as another ClientFamily's client. 
    # i.e. a ClientFamily cant have a family_head that has, itself, a family_head. 
    # See the Alembic migration b2828ec5cf74_add_trigger.py, or, check_client_head_trigger.sql.

    def __repr__(self):
        return f'<ClientFamily {self.client} - {self.family_head}>'

    def __str__(self):
        return f'{self.family_head}: \n{self.client}'

    def toJson(self):
        return {
            "client": self.client,
            "family_head": self.family_head
        }


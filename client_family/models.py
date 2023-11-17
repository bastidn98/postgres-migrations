from flask_sqlalchemy import SQLAlchemy
import boto3
from sqlalchemy import event, DDL
from sqlalchemy.schema import CheckConstraint
import os
from typing import Tuple, Union
from .logger import logging

logger = logging.getLogger(__package__)
db = SQLAlchemy()

class Base:
    """Things common to all models"""

    @classmethod
    def get_fieldnames(cls, excludes=None, excludes_add=None, firsts=[]) -> Tuple[list[str], list[Union[str, None]]]:
        excludes = excludes or cls.excludes
        excludes = list(excludes) + excludes_add if excludes_add else excludes
        if getattr(cls, "optionals", None):
            excludes += cls.optionals
        fieldnames = []
        for prop in cls.__mapper__.iterate_properties:
            if prop.key not in excludes and isinstance(getattr(prop, "argument", ""), str):
                fieldnames.append(prop.key)
        if firsts:
            fieldnames = [fieldnames.pop(fieldnames.index(first)) for first in firsts] + fieldnames
        if getattr(cls, "optionals", None):
            return fieldnames, list(cls.optionals)
        return fieldnames, []

class ClientFamily(Base, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client = db.Column(db.String(), nullable=False, unique=True)
    client_name = db.Column(db.String(), nullable=False, unique=True)
    family_head = db.Column(db.String(), nullable=False)
    family_head_name = db.Column(db.String(), nullable=False)
    excludes = ('id',)
    optionals = ('client_name', 'family_head_name')
    
    # __table_args__= (
    #     CheckConstraint(client!=family_head, name='check_client_head_entry_constraint'),
    # ) Turning this off, potentially temporarily

    # NOTE: There is a database trigger associated with this table that enforces
    # additional constraints. The constraint makes it soa new ClientFamily cant 
    # have a family_head that already exists as another ClientFamily's client. 
    # i.e. a ClientFamily cant have a family_head that has, itself, a family_head. 
    # See the Alembic migration b2828ec5cf74_add_trigger.py, or, check_client_head_trigger.sql.

    def __repr__(self):
        return f'<ClientFamily {self.client} - {self.family_head}>'

    def __str__(self):
        return f'\n{self.client}: {self.family_head}'

    def toJson(self):
        return {
            "client": self.client,
            "family_head": self.family_head,
            "client_name": self.client_name,
            "family_head_name": self.family_head_name
        }


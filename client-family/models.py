from flask_sqlalchemy import SQLAlchemy
import boto3

db = SQLAlchemy()

class ClientFamily(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client = db.Column(db.String(), nullable=False, unique=True)
    family_head = db.Column(db.String(), nullable=False)
    
    

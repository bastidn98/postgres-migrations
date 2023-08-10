from flask_admin import Admin
import os
from logging import getLogger
from .flask_admin import HomePageRedirect, ClassFamilyModelView
from .models import db, ClientFamily

logger = getLogger(__name__)

def init_admin(app):
    '''Adds models to admin frontend'''
    admin = Admin(app, name='SQL Admin', template_mode='bootstrap3',  index_view=HomePageRedirect())
    admin.add_views(
        ClassFamilyModelView(ClientFamily, db.session, name='Client Family', endpoint='client_family'), 
        )
    admin._menu=admin._menu[1:] # XXX remove this if wanting to add home button back 
    logger.info('Added modelviews to Flask-Admin')
    return True

def init_db(app):
    '''Sets up database urls''' 
    if not app.config.get('SQLALCHEMY_DATABASE_URI', None):
        USER = os.environ['POSTGRES_USER']
        PSWD = os.environ['POSTGRES_PSWD']
        HOST = os.environ['POSTGRES_HOST']
        DB = os.environ['POSTGRES_DBNAME']
        
        app.config['SQLALCHEMY_DATABASE_URI']=f'postgresql+psycopg2://{USER}{":"+PSWD if PSWD else ""}@{HOST}/{DB}'
        
    db.init_app(app)
    return True
            
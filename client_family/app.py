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
        match os.getenv('ENV', 'dev').lower():
            case 'prod':
                USER = os.environ['PROD_USER']
                PSWD = os.environ['PROD_PSWD']
                HOST = os.environ['PROD_HOST']
                DB = os.environ['PROD_DBNAME']
            case 'dev':
                USER = 'postgres'
                PSWD = 'postgres'
                HOST = 'localhost:5432'
                DB = os.getenv('LOCAL_DEV_DB', 'devdb')
            case 'test':
                USER = 'postgres'
                PSWD = 'postgres'
                HOST = 'localhost:5432'
                DB = os.getenv('LOCAL_testdb_DB', 'testdb')
            case _:
                raise Exception('Please set "ENV" environment to "prod" or "dev"')
        
        app.config['SQLALCHEMY_DATABASE_URI']=f'postgresql+psycopg2://{USER}{":"+PSWD if PSWD else ""}@{HOST}/{DB}'
        
    db.init_app(app)
    return True
            
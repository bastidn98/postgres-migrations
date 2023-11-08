from flask_admin import Admin
import os
from .logger import logging
from flask_migrate import Migrate, upgrade
from .flask_admin import HomePageRedirect, ClassFamilyModelView
from .models import db, ClientFamily

logger = logging.getLogger(__package__)

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
                logger.info('Connected to PROD database!!')
            case 'dev':
                USER = os.getenv('DEV_USER', 'postgres')
                PSWD = os.getenv('DEV_PSWD', '')
                HOST = os.getenv('DEV_HOST_PORT')
                DB = os.getenv('DEV_DBNAME', 'clientfam')
                logger.info('Connected to DEV database!!')
            case _:
                raise Exception('Please set "ENV" environment to "prod" or "dev"')
        
        app.config['SQLALCHEMY_DATABASE_URI']=f'postgresql+psycopg2://{USER}{":"+PSWD if PSWD else ""}@{HOST}/{DB}'
        
    db.init_app(app)
    return True
            
def init_migrate(app):
    '''Sets up database migrations. Needs to have postgres set as database type, and have "REBUILD_DB" on. 
    Double checks this is in dev environment... just in case. Otherwise need to use "force" option'''
    migrate = Migrate(app, db) # Setting up migrations with alembic 
    if os.environ['REBUILD_DB'].lower() in ('t', 'true', 'yes', 'y', 'force'):
        if os.environ['ENV'].lower() not in ('dev', 'development', 'local'):
            if os.environ['REBUILD_DB'].lower() != 'force':
                logger.error(f'REBUILD_DB is not set to force, but DEPLOY_ENV is not dev (it\'s {os.environ["DEPLOY_ENV"]}). Not rebuilding')
                return False
        with app.app_context():
            db.reflect()
            db.drop_all()
            upgrade()
            logger.info('Dropped and Rebuilt database (no data)')
            return True
    return False
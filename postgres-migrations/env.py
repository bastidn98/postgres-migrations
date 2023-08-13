import logging
from logging.config import fileConfig
from dotenv import load_dotenv

load_dotenv()

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

import os
import logging
from logging.config import fileConfig
from alembic import context
from sqlalchemy import engine_from_config, pool

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')

# Retrieve the DATABASE_URL from the environment
USER = os.getenv('POSTGRES_USER', 'postgres')
PSWD = os.getenv('POSTGRES_PASSWORD', 'postgres')
DB = os.getenv('DB', None)
DATABASE_URL = f'postgresql+psycopg2://{USER}{":"+PSWD if PSWD else ""}@postgres:5432/{DB}'

if not DB:
    raise Exception('DB must be set as an environment variable')

# Add this URL to the Alembic config object
config.set_main_option('sqlalchemy.url', DATABASE_URL)


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=None, literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    configuration = config.get_section(config.config_ini_section)
    configuration['sqlalchemy.url'] = DATABASE_URL
    connectable = engine_from_config(
        configuration,
        prefix='sqlalchemy.',
        poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=None
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
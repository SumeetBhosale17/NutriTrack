import logging
from logging.config import fileConfig

from flask import current_app
from alembic import context

# Alembic Config object
config = context.config

# Setup Python logging
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')

# Import your app and models here
from app import db  # your SQLAlchemy instance
from app.models import *  # import all your models

# Set target metadata for 'autogenerate' support
target_metadata = db.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode (without DB connection)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode (with DB connection)."""

    def process_revision_directives(context, revision, directives):
        """Skip empty migrations."""
        if getattr(config.cmd_opts, "autogenerate", False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                logger.info("No changes in schema detected.")

    connectable = current_app.extensions['migrate'].db.engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            process_revision_directives=process_revision_directives,
            compare_type=True,  # optional: detects column type changes
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

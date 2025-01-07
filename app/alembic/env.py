from logging.config import fileConfig
from sqlalchemy import engine_from_config, text
from sqlalchemy import pool
from alembic import context
import os
from pathlib import Path
from dotenv import load_dotenv

# Get absolute path of .env
env_path = Path(__file__).resolve().parent.parent / ".env"

load_dotenv(env_path)

# Build postgres URL
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT")

SQLALCHEMY_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Alembic config
config = context.config

# Logging config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Load SQLALCHEMY_URL
config.set_main_option("sqlalchemy.url", SQLALCHEMY_URL)

# Import models
from src.models import Base, User, QrCode, Scan

# Set metadata
target_metadata = Base.metadata


def run_migrations_offline() -> None:
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
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata,
            include_schemas=True
        )

        with context.begin_transaction():
            connection.execute(text('CREATE SCHEMA IF NOT EXISTS qr_challenge'))
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

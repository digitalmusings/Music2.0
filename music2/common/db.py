"""
Utilities for working with our database.

The only function that should be used, generally, is `get_db_session`. This
returns a SQLAlchemy Session instance which should already be connected to the
database and ready to use.

The Session will automatically run in a transaction, so can be used directly
like this:

    session = db.get_db_session()

    session.add(...)
    session.execute(...)
    session.commit()

    session.add(...)
    if problem:
        session.rollback()

On the other hand, it is often prudent to be explicit about what runs in a
single transaction using a context manager:

    session = db.get_db_session()

    with session.begin():
        session.add(...)
        session.execute(...)

    with session.begin():
        session.add(...)
        if problem:
            session.rollback()

Note: During testing, each test will be run inside a single transaction and
`Session.commit` will be disabled. If a function relies on a series of commits
being executed, it will likely fail testing and should probably be broken up
anyway.
"""

import functools
import os

import sqlalchemy
import sqlalchemy.orm

from music2.common.exceptions import ConfigError

# DEFAULT_HOST = "musicdb.cpc6p0drvgxc.us-east-1.rds.amazonaws.com"
DEFAULT_HOST = "localhost"
DEFAULT_PORT = 5432
DEFAULT_NAME = "music"

# TODO swap out for config values
DB_HOST = os.getenv("DB_HOST", DEFAULT_HOST)
DB_PORT = os.getenv("DB_PORT", DEFAULT_PORT)
DB_NAME = os.getenv("DB_NAME", DEFAULT_NAME)
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_CONNECT_TIMEOUT = 10  # seconds

__all__ = ("get_db_session",)


def get_db_url(user, password, host=DEFAULT_HOST, port=DEFAULT_PORT, name=DEFAULT_NAME):
    """
    Construct a PostgreSQL database URL for building a SQLAlchemy engine.

    User and password are required, the other options will use default values if
    not specified.
    """

    if not user or not password:
        raise ConfigError(
            "DB_USER and DB_PASSWORD are both required to connect to the database"
        )
    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}"


@functools.cache
def get_db_engine(timeout=DB_CONNECT_TIMEOUT):
    """
    Return a SQLAlchemy DB engine using the configuration values.

    This engine is not opened automatically. To use, first open a connection:

        engine = get_db_engine()
        with engine.connect() as connection:
            connection.execute(query)

    Or start a session:

        engine = get_db_engine()
        session = sqlalchemy.orm.Session(engine)
        session.execute(query)
    """

    url = get_db_url(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)
    return sqlalchemy.create_engine(url, connect_args={"connect_timeout": timeout})


@functools.cache
def get_db_session():
    """
    Returns an open DB session.

    This session is already open and can be used immediately. It will manage
    transactions automatically, but can explicitly start a transaction like this:

        session = get_db_session()
        with session.begin():
            session.execute(query)
    """

    engine = get_db_engine()
    return sqlalchemy.orm.Session(engine)

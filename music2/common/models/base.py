"""
Base model which will contain the registry of all the other SQLAlchemy models

This uses the DeclarativeBase syntax and all other models will inherit from this
Base class directly.

Also included are the following conveniences:
- pk - Annotated type wrapper for UUID for use as a primary key, specifies
    default behaviors
- fk - Annotated type wrapper for UUID for use as an indexed foreign key
- datetime_now - Annotated type wrapper for datetime that sets the server
    default to `now()`
"""

import datetime
import typing
import uuid

import sqlalchemy
from sqlalchemy import orm, schema
from sqlalchemy.dialects import postgresql

__all__ = ("Base",)

# UUID primary key with sane defaults
pk = typing.Annotated[
    uuid.UUID,
    orm.mapped_column(
        primary_key=True,
        server_default=sqlalchemy.text("gen_random_uuid()"),
        default=uuid.uuid4,
    ),
]

# UUID to use when you want an index on your FK
fk = typing.Annotated[uuid.UUID, orm.mapped_column(index=True)]

# datetime that defaults to now()
datetime_now = typing.Annotated[
    datetime.datetime, orm.mapped_column(server_default=sqlalchemy.text("now()"))
]


class Base(orm.DeclarativeBase):
    type_annotation_map = {
        str: sqlalchemy.Text,
        list[str]: mutable.MutableList.as_mutable(postgresql.ARRAY(sqlalchemy.Text)),
    }

    @classmethod
    def _create_table(cls):
        return str(
            schema.CreateTable(cls.__table__).compile(dialect=postgresql.dialect())
        )

"""
Base model which will contain the registry of all the other SQLAlchemy models

This uses the DeclarativeBase syntax and all other models will inherit from this
Base class directly.

Also included are the following conveniences:
- pk - Annotated type wrapper for UUID for use as a primary key, specifies
    default behaviors
- fk - Annotated type wrapper for UUID for use as an indexed foreign key
"""

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


class Base(orm.DeclarativeBase):
    type_annotation_map = {
        str: sqlalchemy.Text,
    }

    @classmethod
    def _create_table(cls):
        return str(
            schema.CreateTable(cls.__table__).compile(dialect=postgresql.dialect())
        )

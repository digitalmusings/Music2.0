"""
SQLAlchemy ORM - Genre, GenreRelation

Each row of the genre table represents a single genre or sub-genre of music that
can be assigned to a certain song or to an artist as a whole.

Genres can have any number of parent or child genres, as indicated in the
genre_relation table.
"""

import sqlalchemy
from sqlalchemy import orm

from music2.models import base

__all__ = ("Genre", "GenreRelation")


class Genre(base.Base):
    __tablename__ = "genre"

    genre_id: orm.Mapped[base.pk]
    name: orm.Mapped[str] = orm.mapped_column(unique=True)


class GenreRelation(base.Base):
    __tablename__ = "genre_relation"

    genre_relation_id: orm.Mapped[base.pk]
    parent_genre_id: orm.Mapped[base.fk | None]
    child_genre_id: orm.Mapped[base.fk | None]

    __table_args__ = (
        sqlalchemy.ForeignKeyConstraint(
            ["parent_genre_id"], ["genre.genre_id"], ondelete="SET NULL"
        ),
        sqlalchemy.ForeignKeyConstraint(
            ["child_genre_id"], ["genre.genre_id"], ondelete="SET NULL"
        ),
    )

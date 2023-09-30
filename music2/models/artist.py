"""
SQLAlchemy ORM - Artist, ArtistGenre

An artist represents any person or group of people operating under a given name.
Each name will have its own row in the artist table, linking to a canonical
"primary" name for that artist if applicable. The artists here represent anyone
involved in the making of the music, performers, composers, remixers, etc.

Additionally, an artist can be tagged with any number of genres via the
artist_genre table.
"""

import sqlalchemy
from sqlalchemy import orm

from music2.models import base

__all__ = ("Artist", "ArtistGenre")


class Artist(base.Base):
    __tablename__ = "artist"

    artist_id: orm.Mapped[base.pk]
    name: orm.Mapped[str]
    year_min: orm.Mapped[int | None]
    year_max: orm.Mapped[int | None]
    primary_artist_id: orm.Mapped[base.fk]

    __table_args__ = (
        sqlalchemy.ForeignKeyConstraint(
            ["primary_artist_id"], ["artist.artist_id"], ondelete="RESTRICT"
        ),
    )


class ArtistGenre(base.Base):
    __tablename__ = "artist_genre"

    artist_genre_id: orm.Mapped[base.pk]
    artist_id: orm.Mapped[base.fk]
    genre_id: orm.Mapped[base.fk]

    __table_args__ = (
        sqlalchemy.UniqueConstraint("artist_id", "genre_id"),
        sqlalchemy.ForeignKeyConstraint(
            ["artist_id"], ["artist.artist_id"], ondelete="CASCADE"
        ),
        sqlalchemy.ForeignKeyConstraint(
            ["genre_id"], ["genre.genre_id"], ondelete="CASCADE"
        ),
    )

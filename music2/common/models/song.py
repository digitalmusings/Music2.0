"""
SQLAlchemy ORM - Song, SongRelation, SongArtist, SongGenre

Each row of the song table represents a single version / performance of a given
song. Each remix, cover, live performance, etc. should have its own row. A given
artist may have a canonical version of a song which remixes and live
performances link to. And a given artist's canonical version which is a cover
can also link further back to a canonical original version. Furthermore, each
song can have any number of individual artists, collaborators, and composers
linked to it.

In general, if submissions from multiple participants correspond to the same
song row, these are duplicates. But multiple submissions that correspond to
separate song rows that are determined to link together somehow (different
performances or versions of a song by a given artist, different covers of a song
by multiple artists, even different mixes of the same song in certain
circumstances), these are not duplicates but in general only one should be
allowed into a bracket. This is usually resolved during a play-in round.

The song_relation table holds links from one song to another, generally either
linking multiple versions of the same song by a single artist to their
canonical, original version, or else linking covers, etc., back to the original
version of a song.

The song_artist table ties multiple artists, with multiple credit types (e.g.
collaborators, remixers, composers), to a single version of a song.

Additionally, a song can be tagged with any number of genres via the song_genre
table.
"""

import sqlalchemy
from sqlalchemy import orm

from music2.common.models import base

__all__ = ("Song", "SongArtist", "SongGenre", "SongRelation")


class Song(base.Base):
    __tablename__ = "song"

    song_id: orm.Mapped[base.pk]
    title: orm.Mapped[str]
    title_english: orm.Mapped[str | None]
    version: orm.Mapped[str | None]
    artist: orm.Mapped[str] = orm.mapped_column(comment="CALCULATED")
    collaborator: orm.Mapped[str | None] = orm.mapped_column(comment="CALCULATED")
    composer: orm.Mapped[str | None]
    year: orm.Mapped[int | None]
    year_alt: orm.Mapped[int | None]


class SongRelation(base.Base):
    __tablename__ = "song_relation"

    song_relation_id: orm.Mapped[base.pk]
    parent_song_id: orm.Mapped[base.fk]
    child_song_id: orm.Mapped[base.fk]
    song_relation_type: orm.Mapped[str] = orm.mapped_column(comment="cover live alternate")

    __table_args__ = (
        sqlalchemy.ForeignKeyConstraint(
            ["parent_song_id"], ["song.song_id"], ondelete="CASCADE"
        ),
        sqlalchemy.ForeignKeyConstraint(
            ["child_song_id"], ["song.song_id"], ondelete="CASCADE"
        ),
    )


class SongArtist(base.Base):
    __tablename__ = "song_artist"

    song_artist_id: orm.Mapped[base.pk]
    song_id: orm.Mapped[base.fk]
    artist_id: orm.Mapped[base.fk]
    credit_type: orm.Mapped[str] = orm.mapped_column(
        comment="primary collaborator original remixer composer"
    )

    __table_args__ = (
        sqlalchemy.UniqueConstraint("song_id", "artist_id"),
        sqlalchemy.ForeignKeyConstraint(
            ["song_id"], ["song.song_id"], ondelete="CASCADE"
        ),
        sqlalchemy.ForeignKeyConstraint(
            ["artist_id"], ["artist.artist_id"], ondelete="CASCADE"
        ),
    )


class SongGenre(base.Base):
    __tablename__ = "song_genre"

    song_genre_id: orm.Mapped[base.pk]
    song_id: orm.Mapped[base.fk]
    genre_id: orm.Mapped[base.fk]

    __table_args__ = (
        sqlalchemy.UniqueConstraint("song_id", "genre_id"),
        sqlalchemy.ForeignKeyConstraint(
            ["song_id"], ["song.song_id"], ondelete="CASCADE"
        ),
        sqlalchemy.ForeignKeyConstraint(
            ["genre_id"], ["genre.genre_id"], ondelete="CASCADE"
        ),
    )

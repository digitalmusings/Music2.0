"""
SQLAlchemy ORM - Song

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
"""

from sqlalchemy import orm

from music2.models import base

__all__ = ("Song",)


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
